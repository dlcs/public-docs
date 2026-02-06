import settings
from iiif_cs import put_resource, pprint


def put_asset():
    asset = {
      "mediaType": "image/jpeg",
      "origin": "https://dlcs.github.io/public-docs/doc_fixtures/rusty-boat.jpg"
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/1/put-example-1-rusty-boat"
    r = put_resource(path, asset)


if __name__ == '__main__':
    put_asset()