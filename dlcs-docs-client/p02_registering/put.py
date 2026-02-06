import settings
from iiif_cs import put_resource, pprint

def put_asset():
    asset = {
      "mediaType": "image/jpeg",
      "origin": "https://dlcs.github.io/public-docs/_astro/houston.CZZyCf7p_ZV2VG3.webp"
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/1/put-example-rusty-boat"

if __name__ == '__main__':
    put_asset()