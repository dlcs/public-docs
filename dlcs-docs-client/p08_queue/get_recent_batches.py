import settings
from iiif_cs import get_cloud_services_resource, pprint


def get_recent_batches():
    """GET the collection of batches that have finished processing."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue/recent"
    r = get_cloud_services_resource(path)
    print("GET Recent Batches returned:")
    batches = r.json()
    pprint(batches)
    print()
    return batches


if __name__ == '__main__':
    get_recent_batches()
