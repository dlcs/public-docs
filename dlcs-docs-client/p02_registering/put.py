import settings
from iiif_cs import put_resource, pprint
from p06_space.ensure_space import ensure_space


def put_asset():
    space = 1
    ensure_space(space, "Space created by documentation example")
    asset = {
      "mediaType": "image/jpeg",
      "origin": "https://dlcs.github.io/public-docs/doc_fixtures/rusty-boat.jpg"
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space}/images/put-example-1-rusty-boat"
    r = put_resource(path, asset)
    print("PUT returned:")
    pprint(r.json())
    print()


if __name__ == '__main__':
    put_asset()