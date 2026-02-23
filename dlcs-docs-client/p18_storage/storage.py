import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, pprint


def get_customer_storage():
    """GET the storage usage summary for the whole customer account."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/storage"
    r = get_cloud_services_resource(path)
    storage = r.json()
    print("GET customer storage returned:")
    pprint(storage)
    print()
    return storage


def get_space_storage(space_id=docs_space_id):
    """GET the storage usage summary for a single space."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/storage"
    r = get_cloud_services_resource(path)
    storage = r.json()
    print("GET space storage returned:")
    pprint(storage)
    print()
    return storage


def get_image_storage(asset_id, space_id=docs_space_id):
    """GET the storage usage for a single asset."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}/storage"
    r = get_cloud_services_resource(path)
    storage = r.json()
    print("GET image storage returned:")
    pprint(storage)
    print()
    return storage


def get_storage_policy(customer_storage):
    """Follow the storagePolicy link from a CustomerStorage resource."""
    policy_url = customer_storage["storagePolicy"]
    r = get_cloud_services_resource(policy_url)
    policy = r.json()
    print("GET storagePolicy returned:")
    pprint(policy)
    print()
    return policy


if __name__ == '__main__':
    # GET customer-wide storage usage
    customer_storage = get_customer_storage()

    # GET storage usage for one space
    get_space_storage()

    # GET storage usage for a single asset (the rusty boat registered in p02_registering/put.py)
    get_image_storage("put-example-1-rusty-boat")

    # Follow the storagePolicy link to see the customer's storage limit
    get_storage_policy(customer_storage)
