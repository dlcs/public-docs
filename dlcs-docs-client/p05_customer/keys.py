import settings
from iiif_cs import get_cloud_services_resource, post_resource, pprint, delete_resource


def get_keys():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/keys"
    keys = get_cloud_services_resource(path).json()
    print("GET returned:")
    pprint(keys)
    print()


def create_key():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/keys"
    r = post_resource(path, None)
    print("POST returned:")
    key = r.json()
    pprint(key)
    print()
    return key['@id']


if __name__ == '__main__':
    get_keys()
    key_uri = create_key()
    get_keys()
    delete_resource(key_uri)
    get_keys()
