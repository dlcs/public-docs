import settings
from iiif_cs import get_cloud_services_resource, post_resource, pprint
from settings import docs_space_id


def get_adjunct_queue():
    """GET the customer adjunct queue to see its current status."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/adjunctQueue"
    r = get_cloud_services_resource(path)
    print("GET Adjunct Queue returned:")
    queue = r.json()
    pprint(queue)
    print()
    return queue


def post_to_adjunct_queue(asset_id, space_id=docs_space_id):
    """POST a collection of adjuncts to the adjunct queue for processing."""
    # A collection with one or more adjuncts to register
    collection = {
        "member": [
            {
                "id": "queue-adjunct-example.txt",
                "space": space_id,
                "image": asset_id,
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/adjuncts/rusty-boat.txt",
                "@type": "Text",
                "mediaType": "text/plain",
                "label": {"en": ["Example adjunct via queue"]},
                "iiifLink": "seeAlso",
                "language": ["en"]
            }
        ]
    }

    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/adjunctQueue"
    r = post_resource(path, collection)
    print("POST to Adjunct Queue returned:")
    batch = r.json()  # The response is an AdjunctBatch resource
    pprint(batch)
    print()
    return batch


if __name__ == '__main__':
    # Get the current adjunct queue status
    get_adjunct_queue()
