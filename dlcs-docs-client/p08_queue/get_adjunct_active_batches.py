import settings
from iiif_cs import get_cloud_services_resource, pprint


def get_adjunct_active_batches():
    """GET the collection of adjunct batches currently being processed."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/adjunctQueue/active"
    r = get_cloud_services_resource(path)
    print("GET Active Adjunct Batches returned:")
    batches = r.json()
    pprint(batches)
    print()
    return batches


if __name__ == '__main__':
    get_adjunct_active_batches()
