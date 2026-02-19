import requests
import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, pprint

# The single asset manifest is a public-facing resource served by the IIIF host,
# not the API host. Derive the public host by removing the 'api.' subdomain.
public_host = settings.IIIF_CS_API_HOST.replace("//api.", "//", 1)

# The rusty boat asset registered in p02_registering/put.py
asset_id = "put-example-1-rusty-boat"


def get_asset(asset_id=asset_id, space_id=docs_space_id):
    """GET an asset from the API to inspect its properties."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}"
    r = get_cloud_services_resource(path)
    print("GET Asset returned:")
    asset = r.json()
    pprint(asset)
    print()
    return asset


def get_single_asset_manifest(asset_id=asset_id, space_id=docs_space_id):
    """Retrieve the single asset manifest. This is a public IIIF resource served
    by the platform, not the API - no API credentials are required.

    The URL pattern is:
        {public-host}/iiif-manifest/{customer}/{space}/{asset-id}
    """
    manifest_url = f"{public_host}/iiif-manifest/{settings.IIIF_CS_CUSTOMER_ID}/{space_id}/{asset_id}"
    print("-------------------------------------------")
    print(f"GET {manifest_url}")
    r = requests.get(manifest_url)
    print(f"HTTP Status Code: {r.status_code}")
    print("Single asset manifest returned:")
    pprint(r.json())
    print()
    return r.json()


if __name__ == '__main__':
    # GET the asset from the API to see its delivery channels
    get_asset()

    # GET the public-facing single asset manifest
    get_single_asset_manifest()
