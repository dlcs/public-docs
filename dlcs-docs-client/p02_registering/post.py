import settings
from iiif_cs import post_resource, pprint
from p06_space.ensure_space import ensure_space

# Not yet supported. Returns HTTP 405 Method Not Allowed
def post_asset():
    space = 1
    ensure_space(1, "Space created by documentation example")
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