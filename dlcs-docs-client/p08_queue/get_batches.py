import settings
from iiif_cs import get_cloud_services_resource, pprint


def get_batches():
    """GET the collection of batches for this customer."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue/batches"
    r = get_cloud_services_resource(path)
    print("GET Batches returned:")
    batches = r.json()
    pprint(batches)
    print()
    return batches


if __name__ == '__main__':
    get_batches()
