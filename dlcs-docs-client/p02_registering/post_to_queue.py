import settings
from iiif_cs import post_resource, pprint, get_cloud_services_resource
from p06_space.ensure_space import ensure_space


def post_asset_to_queue():
    space = 1
    ensure_space(1, "Space created by documentation example")
    collection = {
      "member": [
        {
          "id": "post-to-queue-example-1-rhine",
          "space": space,
          "mediaType": "image/jpeg",
          "origin": "https://dlcs.github.io/public-docs/doc_fixtures/by-the-rhine.jpg"
        }
      ]
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue"
    r = post_resource(path, collection)
    print("POST returned:")
    batch = r.json() # We expect this to be a batch
    pprint(batch)
    print()

    print(f"Response was a batch with @id {batch['@id']}")
    batch_again = get_cloud_services_resource(batch['@id'])
    pprint(batch_again.json())
    print()




if __name__ == '__main__':
    post_asset_to_queue()