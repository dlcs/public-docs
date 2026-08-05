import settings
from iiif_cs import post_resource, pprint
from p06_space.ensure_space import ensure_space
from settings import docs_space_id, docs_space_name


# INTENTIONAL error demo - this sample is *supposed* to fail.
# Direct POST of a single asset to a space is not supported; the platform
# returns HTTP 405 Method Not Allowed. Register assets with PUT, or POST a
# collection to the queue instead (see registering-assets).
def post_asset():
    space = docs_space_id
    ensure_space(space, docs_space_name)
    asset = {
      "id": "post-example-1-rusty-boat",
      "mediaType": "image/jpeg",
      "origin": "https://dlcs.github.io/public-docs/doc_fixtures/rusty-boat.jpg"
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space}/images"
    r = post_resource(path, asset)
    print("POST returned:")
    pprint(r.json())
    print()


if __name__ == '__main__':
    post_asset()