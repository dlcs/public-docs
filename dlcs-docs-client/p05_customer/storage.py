import settings
from iiif_cs import get_cloud_services_resource, post_resource, pprint


def get_storage():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/storage"
    storage = get_cloud_services_resource(path).json()
    print("GET returned:")
    pprint(storage)
    print()


if __name__ == '__main__':
    get_storage()