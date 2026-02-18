import settings
from iiif_cs import get_cloud_services_resource, post_resource, pprint
from p06_space.ensure_space import ensure_space
from settings import docs_space_id, docs_space_name


def get_queue():
    """GET the customer queue to see its current status."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue"
    r = get_cloud_services_resource(path)
    print("GET Queue returned:")
    queue = r.json()
    pprint(queue)
    print()
    return queue


def post_to_queue():
    """POST a collection of assets to the queue for processing."""
    ensure_space(docs_space_id, docs_space_name)

    # A collection with one or more assets to register
    collection = {
        "member": [
            {
                "id": "queue-example-1",
                "space": docs_space_id,
                "mediaType": "image/jpeg",
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/by-the-rhine.jpg"
            }
        ]
    }

    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue"
    r = post_resource(path, collection)
    print("POST to Queue returned:")
    batch = r.json()  # The response is a Batch resource
    pprint(batch)
    print()
    return batch


if __name__ == '__main__':
    # Get the current queue status
    get_queue()

    # Post an asset to the queue
    post_to_queue()

    # Get the queue again to see the change
    get_queue()
