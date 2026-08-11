# SPA-10 in-room live check (hygiene sprint session 2). MUTATING - run deliberately.
#
# Question: does a no-op PUT to an asset always trigger reingest (code trace says yes:
# CreateOrUpdateImage.cs:50 sets AlwaysReingest for PUT), where the docs imply
# reprocessing happens only when `origin` changes?
#
# What it does, in the docs space on the configured deployment:
#   1. PUT a throwaway image asset and wait for ingestion to finish.
#   2. Record its `finished` timestamp.
#   3. PUT the identical body again (a no-op replace).
#   4. Report whether the asset went back into processing (finished cleared/advanced).
#   5. DELETE the asset.
#
# Run from the dlcs-docs-client directory:
#   python ../scratch/hygiene-sprint/tools/spa10_put_reingest_check.py

import sys
import time

sys.path.insert(0, ".")  # expect to be run from dlcs-docs-client/

import settings
from iiif_cs import get_cloud_services_resource, put_resource, delete_resource, pprint

ASSET_ID = "hygiene-spa10-reingest-check"
PATH = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{settings.docs_space_id}/images/{ASSET_ID}"
BODY = {
    "origin": "https://iiif.io/api/image/3.0/example/reference/918ecd18c2592080851777620de9bcb5-gottingen/full/max/0/default.jpg",
    "mediaType": "image/jpeg",  # PUT validates with the create ruleset: mediaType required every time
}


def wait_until_finished(label, retries=30, interval=2):
    for _ in range(retries):
        asset = get_cloud_services_resource(PATH).json()
        if asset.get("finished"):
            print(f"{label}: ingestion finished at {asset['finished']}")
            return asset
        time.sleep(interval)
    print(f"{label}: WARNING - not finished after {retries * interval}s")
    return get_cloud_services_resource(PATH).json()


if __name__ == "__main__":
    print("1) Initial PUT (registers the asset)")
    r = put_resource(PATH, BODY)
    print(f"   HTTP {r.status_code}")
    first = wait_until_finished("   first ingest")

    print("2) No-op PUT (identical body)")
    r = put_resource(PATH, BODY)
    print(f"   HTTP {r.status_code}")
    immediately_after = get_cloud_services_resource(PATH).json()
    print(f"   finished immediately after second PUT: {immediately_after.get('finished')!r}")
    second = wait_until_finished("   second ingest")

    print()
    if second.get("finished") != first.get("finished"):
        print("RESULT: no-op PUT DID reingest (finished timestamp changed)"
              " - matches the code trace; docs need the PUT/PATCH distinction.")
    else:
        print("RESULT: finished timestamp unchanged - no reingest observed;"
              " re-examine the code trace against this deployment's version.")

    print("3) Cleanup: DELETE")
    delete_resource(PATH)
