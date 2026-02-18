import settings
from iiif_cs import get_cloud_services_resource, pprint


def get_active_batches():
    """GET the collection of batches currently being processed."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue/active"
    r = get_cloud_services_resource(path)
    print("GET Active Batches returned:")
    batches = r.json()
    pprint(batches)
    print()
    return batches


if __name__ == '__main__':
    get_active_batches()
