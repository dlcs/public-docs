import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, put_resource, delete_resource, pprint, patch_resource

# An example asset ID for demonstration
example_asset_id = "docs-example-image"

# A publicly accessible test image
example_origin = "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Image_created_with_a_mobile_phone.png/1200px-Image_created_with_a_mobile_phone.png"


def get_asset(asset_id=example_asset_id, space_id=docs_space_id):
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}"
    asset = get_cloud_services_resource(path).json()
    print("GET Asset returned")
    pprint(asset)
    print()
    return asset


def put_new_asset(asset_id=example_asset_id, space_id=docs_space_id):
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}"
    asset = {
        "mediaType": "image/png",
        "origin": example_origin
    }
    r = put_resource(path, asset)
    pprint(r.json())
    print()
    return r


def put_existing_asset(asset_id=example_asset_id, space_id=docs_space_id):
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}"
    asset = {
        "mediaType": "image/png",
        "origin": example_origin,
        "string1": "updated-value"
    }
    r = put_resource(path, asset)
    pprint(r.json())
    print()
    return r


def patch_asset(asset_id=example_asset_id, space_id=docs_space_id):
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}"
    asset = {
        "string1": "patched-value",
        "tags": ["documentation", "example"]
    }
    r = patch_resource(path, asset)
    pprint(r.json())
    print()
    return r


def delete_asset(asset_id=example_asset_id, space_id=docs_space_id):
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}"
    delete_resource(path)


if __name__ == '__main__':
    # Test all HTTP operations
    # Expected: PUT 201 Created (new asset)
    put_new_asset()
    # Expected: GET 200 OK
    get_asset()
    # Expected: PUT 200 OK (replace existing)
    put_existing_asset()
    # Expected: PATCH 200 OK
    patch_asset()
    # Expected: GET 200 OK (verify patch)
    get_asset()
    # Expected: DELETE 200 OK
    delete_asset()
    # Expected: GET 404 Not Found (asset deleted)
    get_asset()
