import time
import requests
import settings
from iiif_cs import (get_iiif_resource, put_iiif_resource, delete_iiif_resource,
                     delete_resource, pprint)

customer = settings.IIIF_CS_CUSTOMER_ID
host = settings.IIIF_CS_PRESENTATION_HOST
root = f"{host}/{customer}/collections/root"
space = settings.docs_space_id

# Build a manifest from two existing assets plus one NEW asset, registered
# through the manifest itself. The new asset's object is a normal asset
# registration - origin, mediaType and so on.
# (Each new asset currently needs an explicit "space" - see iiif-presentation
# issue #668; they are intended to default to the manifest's own space.)
manifest = {
    "type": "Manifest",
    "label": {"en": ["A manifest from assets"]},
    "slug": "docs-manifest-from-assets",
    "parent": root,
    "paintedResources": [
        {
            "asset": {"id": "page_01", "space": space},
            "canvasPainting": {"canvasOrder": 0, "label": {"en": ["Page 1 (existing asset)"]}}
        },
        {
            "asset": {"id": "page_02", "space": space},
            "canvasPainting": {"canvasOrder": 1, "label": {"en": ["Page 2 (existing asset)"]}}
        },
        {
            "asset": {
                "id": "page_04",
                "space": space,
                "mediaType": "image/jpeg",
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/04.jpg"
            },
            "canvasPainting": {"canvasOrder": 2, "label": {"en": ["Page 4 (a NEW asset)"]}}
        }
    ]
}

r = put_iiif_resource(f"/{customer}/manifests/docs-manifest-from-assets", manifest)
print(f"Create returned {r.status_code} (202 = accepted, ingest in progress)")
print("ingesting:", r.json().get("ingesting"))
print()

# Poll the manifest until the ingesting property disappears
while True:
    r = get_iiif_resource(f"/{customer}/manifests/docs-manifest-from-assets")
    ingesting = r.json().get("ingesting")
    print("poll - ingesting:", ingesting)
    if not ingesting:
        break
    time.sleep(5)
print()

# The public manifest now has three canvases, each painting an image service
public = requests.get(r.json()["publicId"]).json()
print(f"Public manifest has {len(public['items'])} canvases:")
for canvas in public["items"]:
    body = canvas["items"][0]["items"][0]["body"]
    print("  ", canvas["label"]["en"][0], "->", body["id"])
print()

# Clean up: delete the manifest, then the asset it registered.
# Deleting a manifest does NOT delete its assets.
r = get_iiif_resource(f"/{customer}/manifests/docs-manifest-from-assets")
d = delete_iiif_resource(f"/{customer}/manifests/docs-manifest-from-assets", r.headers["ETag"])
print(f"DELETE manifest: {d.status_code}")
d = delete_resource(f"/customers/{customer}/spaces/{space}/images/page_04")
print(f"DELETE the newly registered asset: {d.status_code}")
