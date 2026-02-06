import settings
from iiif_cs import get_resource, pprint

def get_iiif_cs_root():
    api_root = get_resource("/").json()
    print("API Root:")
    pprint(api_root)
    print()

    customers = get_resource(api_root["customers"]).json()
    print("All customers:")
    pprint(customers)
    print()

    other_customer = get_resource(customers['member'][0]['@id'])
    print("HTTP status code when requesting a different customer:")
    print(other_customer.status_code)
    print()

    self_customer = get_resource(f"/customers/{settings.IIIF_CS_CUSTOMER_ID}").json()
    print("Response when requesting own customer resource:")
    pprint(self_customer)
    print()

if __name__ == '__main__':
    get_iiif_cs_root()