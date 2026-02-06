import settings
from iiif_cs import get_resource, pprint

def demonstrate_navigation_properties():

    # Get the API root
    api_root = get_resource("/").json()
    print("API Root:")
    pprint(api_root)
    print()

    # navigate to the customers resource
    customers = get_resource(api_root["customers"]).json()
    pprint(customers)
    print()

    # Load a customer who isn't you
    print("HTTP status code when requesting a different customer:")
    other_customer = get_resource(customers['member'][0]['@id'])
    print(other_customer.status_code)
    print()

    # Load your customer resource
    print("Response when requesting own customer resource:")
    self_customer = get_resource(f"/customers/{settings.IIIF_CS_CUSTOMER_ID}").json()
    pprint(self_customer)
    print()

if __name__ == '__main__':
    demonstrate_navigation_properties()