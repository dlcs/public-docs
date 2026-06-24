import settings
from iiif_cs import get_cloud_services_resource, pprint


def get_adjunct_recent_batches():
    """GET the collection of adjunct batches that have finished processing."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/adjunctQueue/recent"
    r = get_cloud_services_resource(path)
    print("GET Recent Adjunct Batches returned:")
    batches = r.json()
    pprint(batches)
    print()
    return batches


if __name__ == '__main__':
    get_adjunct_recent_batches()
