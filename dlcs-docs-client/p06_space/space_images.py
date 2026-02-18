import settings
from settings import docs_space_id, docs_space_name
from iiif_cs import pprint, get_cloud_services_resource, post_resource, delete_resource
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


# Not yet supported. Returns HTTP 405 Method Not Allowed
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


# TODO: Unsupported - same as customer.allImages
# def patch_images_with_query():

# TODO: Unsupported - same as customer.allImages
# def patch_images_with_members():


if __name__ == '__main__':
    get_images()
    get_images_with_query()
    # bridge = post_asset()
    get_images()