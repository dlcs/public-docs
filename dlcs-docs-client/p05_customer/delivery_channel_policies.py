import settings
from iiif_cs import get_cloud_services_resource, post_resource, pprint


def get_delivery_channel_policies():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/deliveryChannelPolicies"
    delivery_channel_policies = get_cloud_services_resource(path).json()
    print("GET returned:")
    pprint(delivery_channel_policies) # TODO: this doesn't show the nested members - claims there are no nested members.
    print()
    path = path + "/thumbs"
    thumbs_delivery_channel_policies = get_cloud_services_resource(path).json()
    print("GET returned:")
    pprint(thumbs_delivery_channel_policies)
    print()


def post_delivery_channel_policy():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/deliveryChannelPolicies/thumbs"
    delivery_channel_policy = {
        "name": "my-custom-thumbs", # TODO: why not "id" for consistency?
        "displayName": "Standard set of thumbs for use on our website",
        "channel": "thumbs",
        "policyData": "[ \"2048,\", \"1336,\", \"880,\", \"^!1024,1024\", \"^!400,400\", \"^,250\" ]"
    }
    r = post_resource(path, delivery_channel_policy)
    print("POST returned:")
    pprint(r.json())
    print()


if __name__ == '__main__':
    get_delivery_channel_policies()
    # post_delivery_channel_policy()