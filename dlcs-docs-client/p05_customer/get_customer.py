import settings
from iiif_cs import get_cloud_services_resource, pprint


def get_customer():
    customer_path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}"
    me = get_cloud_services_resource(customer_path).json()
    pprint(me)


if __name__ == '__main__':
    get_customer()