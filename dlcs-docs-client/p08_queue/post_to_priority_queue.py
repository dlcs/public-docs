import settings
from iiif_cs import post_resource, pprint
from p06_space.ensure_space import ensure_space
from settings import docs_space_id, docs_space_name


def post_to_priority_queue():
    """POST a collection of assets to the priority queue for faster processing."""
    ensure_space(docs_space_id, docs_space_name)

    # A collection with one or more assets to register
    collection = {
        "member": [
            {
                "id": "priority-queue-example-1",
                "space": docs_space_id,
                "mediaType": "image/jpeg",
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/by-the-rhine.jpg"
            }
        ]
    }

    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue/priority"
    r = post_resource(path, collection)
    print("POST to Priority Queue returned:")
    batch = r.json()  # The response is a Batch resource
    pprint(batch)
    print()
    return batch


if __name__ == '__main__':
    post_to_priority_queue()
