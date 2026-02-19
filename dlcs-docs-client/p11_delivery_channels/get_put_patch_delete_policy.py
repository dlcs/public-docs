import settings
from iiif_cs import get_cloud_services_resource, put_resource, patch_resource, delete_resource, pprint

# The policy is identified by channel and a custom name, which becomes the last path element
policy_channel = "thumbs"
policy_name = "docs-example-thumbs"


def get_policy(channel=policy_channel, name=policy_name):
    """GET a DeliveryChannelPolicy by channel and name."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/deliveryChannelPolicies/{channel}/{name}"
    r = get_cloud_services_resource(path)
    print("GET DeliveryChannelPolicy returned:")
    pprint(r.json())
    print()
    return r


def put_policy(channel=policy_channel, name=policy_name):
    """PUT a DeliveryChannelPolicy. Creates if new (201), replaces if it already exists (200).
    Note: 'name' is not included in the body - it comes from the URL path."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/deliveryChannelPolicies/{channel}/{name}"
    policy = {
        "channel": channel,
        "displayName": "Example thumbnail policy",
        "policyData": "[ \"!1024,1024\", \"!400,400\", \"!200,200\", \"!100,100\" ]"
    }
    r = put_resource(path, policy)
    print("PUT DeliveryChannelPolicy returned:")
    pprint(r.json())
    print()
    return r


def patch_policy(channel=policy_channel, name=policy_name):
    """PATCH a DeliveryChannelPolicy, updating only the supplied fields."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/deliveryChannelPolicies/{channel}/{name}"
    patch = {
        "displayName": "Updated thumbnail policy",
        "policyData": "[ \"!1024,1024\", \"!400,400\", \"!200,200\", \"!100,100\", \"!50,50\" ]"
    }
    r = patch_resource(path, patch)
    print("PATCH DeliveryChannelPolicy returned:")
    pprint(r.json())
    print()
    return r


def delete_policy(channel=policy_channel, name=policy_name):
    """DELETE a DeliveryChannelPolicy."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/deliveryChannelPolicies/{channel}/{name}"
    delete_resource(path)


if __name__ == '__main__':
    # Expected: PUT 201 Created (new policy)
    put_policy()
    # Expected: GET 200 OK
    get_policy()
    # Expected: PUT 200 OK (replace existing)
    put_policy()
    # Expected: PATCH 200 OK
    patch_policy()
    # Expected: GET 200 OK (verify patch)
    get_policy()
    # Expected: DELETE 202 Accepted
    delete_policy()
    # Expected: GET 404 Not Found (policy deleted)
    get_policy()
