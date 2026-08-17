import settings
from iiif_cs import put_resource, pprint
from p06_space.ensure_space import ensure_space
from settings import docs_space_id, docs_space_name


# A PUT always causes the platform to (re-)process the asset - fetching it
# from origin and regenerating its outputs - even if nothing in the body
# changed. Re-running this sample re-processes the asset each time.
# See the Reprocessing page of the documentation.
def put_asset():
    space = docs_space_id
    ensure_space(space, docs_space_name)
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