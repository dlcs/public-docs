import settings
from iiif_cs import get_cloud_services_resource, pprint
from p05_customer.delivery_channel_policies import get_delivery_channel_policies


def get_all_delivery_channel_policies():
    """GET the top-level deliveryChannelPolicies collection, then follow each
    child collection link to list all available policies for the customer."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/deliveryChannelPolicies"
    r = get_cloud_services_resource(path)
    top_level = r.json()
    print("GET DeliveryChannelPolicies returned:")
    pprint(top_level)
    print()

    # Each member is itself a collection of policies for that channel
    for channel_collection in top_level.get("member", []):
        r = get_cloud_services_resource(channel_collection["@id"])
        channel_policies = r.json()
        print(f"Policies for '{channel_collection.get('title', channel_collection['@id'])}':")
        pprint(channel_policies)
        print()


if __name__ == '__main__':
    get_delivery_channel_policies()
    get_all_delivery_channel_policies()
