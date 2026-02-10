import settings
from iiif_cs import post_resource, pprint, wait_for_value, get_cloud_services_resource
from p06_space.ensure_space import ensure_space


def get_queue():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue"
    queue = get_cloud_services_resource(path).json()
    print("GET returned:")
    pprint(queue)
    print()


def queue_multiple_assets():
    space = 1
    ensure_space(space, "Space created by documentation example")
    collection = {
      "@type": "hydra:Collection",
      "member": [
        {
          "id": "page_04",
          "space": space,
          "mediaType": "image/jpeg",
          "origin": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/04.jpg",
          "string1": "catalogue-1985",
          "number1": 4
        },
        {
          "id": "page_05",
          "space": space,
          "mediaType": "image/jpeg",
          "origin": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/05.jpg",
          "string1": "catalogue-1985",
          "number1": 5
        },
        {
          "id": "page_06",
          "space": space,
          "mediaType": "image/jpeg",
          "origin": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/06.jpg",
          "string1": "catalogue-1985",
          "number1": 6
        }
      ]
    }

    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue"
    r = post_resource(path, collection)
    print("POST returned:")
    batch = r.json() # We expect this to be a batch
    pprint(batch)
    print(f"Batch {batch['@id']} has {batch['count']} items")
    print()

    wait_for_value(path=batch['@id'], field="completed", value=3, interval=1, retries=5)
    print("All three images should now be processed and available")


if __name__ == '__main__':
    get_queue()
    # queue_multiple_assets()