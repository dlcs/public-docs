import settings
from iiif_cs import get_cloud_services_resource, pprint

def get_entrypoint():

    # Get the API root
    api_root = get_cloud_services_resource("/").json()
    print("API Root:")
    pprint(api_root)
    print()

    # navigate to the customers resource
    customers = get_cloud_services_resource(api_root["customers"]).json()
    pprint(customers)
    print()

    # navigate to the global origin strategies
    origin_strategies = get_cloud_services_resource(api_root["originStrategies"]).json()
    pprint(origin_strategies)
    print()

    # navigate to the global storage policies
    storage_policies = get_cloud_services_resource(api_root["storagePolicies"]).json()
    pprint(storage_policies)
    print()

    # navigate to the global queue
    # queue = get_cloud_services_resource(api_root["queue"]).json() # TODO: add this property
    queue = get_cloud_services_resource(api_root["@id"] + "/queue").json()
    pprint(queue)
    print()



if __name__ == '__main__':
    get_entrypoint()