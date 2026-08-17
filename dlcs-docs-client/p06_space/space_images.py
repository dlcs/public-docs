import settings
from settings import docs_space_id, docs_space_name
from iiif_cs import pprint, get_cloud_services_resource, post_resource, patch_resource, put_resource, delete_resource
from p06_space.ensure_space import ensure_space


def get_images(space:int=docs_space_id, ensure_space_exists:bool=True):
    if ensure_space_exists:
        ensure_space(space, docs_space_name)
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space}/images"
    r = get_cloud_services_resource(path)
    print("GET returned:")
    images = r.json() # We expect this to be a batch
    pprint(images)
    print()
    return images


def get_images_with_query():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{docs_space_id}/images"
    # replace with your own example values
    query = '?q={"string1":"catalogue-1985"}' # or ?string1=catalogue-1985
    r = get_cloud_services_resource(path + query)
    print("GET returned:")
    images = r.json()
    pprint(images)
    print(f"{len(images['member'])} assets returned.")
    print()


# INTENTIONAL error demo - this sample is *supposed* to fail.
# Direct POST of a single asset to a space is not supported; the platform
# returns HTTP 405 Method Not Allowed. Register assets with PUT, or POST a
# collection to the queue instead (see registering-assets).
def post_asset():
    ensure_space(docs_space_id, docs_space_name)
    asset = {
      "id": "post-space-images-ny",
      "mediaType": "image/jpeg",
      "origin": "https://dlcs.github.io/public-docs/doc_fixtures/under-the-bridge.jpg"
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{docs_space_id}/images"
    r = post_resource(path, asset)
    print("POST returned:")
    new_asset = r.json()
    pprint(new_asset)
    print()
    return new_asset


def register_bulk_patch_examples():
    ensure_space(docs_space_id, docs_space_name)
    fixtures = {
        "bulk-patch-example-1": "https://dlcs.github.io/public-docs/doc_fixtures/rusty-boat.jpg",
        "bulk-patch-example-2": "https://dlcs.github.io/public-docs/doc_fixtures/under-the-bridge.jpg"
    }
    for asset_id, origin in fixtures.items():
        asset = {
            "mediaType": "image/jpeg",
            "origin": origin
        }
        path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{docs_space_id}/images/{asset_id}"
        r = put_resource(path, asset)
        print(f"PUT {asset_id} returned HTTP {r.status_code}")
    print()


def bulk_patch_images():
    """Update one or more assets in a single synchronous call.

    The body is a Hydra Collection; each member identifies an asset by id and
    supplies the fields to change. Only fields that do not require the asset to
    be reprocessed may be set - metadata fields like string1, number1, roles or
    tags. Assets are updated one at a time; if a member fails, updates already
    applied to earlier members are not rolled back.
    """
    body = {
        "@type": "Collection",
        "member": [
            {"id": "bulk-patch-example-1", "string1": "bulk-patched"},
            {"id": "bulk-patch-example-2", "string1": "bulk-patched"}
        ]
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{docs_space_id}/images"
    r = patch_resource(path, body)
    print("PATCH returned:")
    patched = r.json()
    pprint(patched)
    print()
    return patched


# INTENTIONAL error demo - this sample is *supposed* to fail.
# Fields that would require the asset to be reprocessed (origin, deliveryChannels,
# maxWidth etc) cannot be set in a bulk patch; the platform returns 400 Bad Request.
def bulk_patch_rejected_field():
    body = {
        "@type": "Collection",
        "member": [
            {"id": "bulk-patch-example-1", "origin": "https://dlcs.github.io/public-docs/doc_fixtures/under-the-bridge.jpg"}
        ]
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{docs_space_id}/images"
    r = patch_resource(path, body)
    print("PATCH with origin returned:")
    pprint(r.json())
    print()


if __name__ == '__main__':
    get_images()
    get_images_with_query()
    # bridge = post_asset()
    register_bulk_patch_examples()
    bulk_patch_images()
    bulk_patch_rejected_field()
    get_images()