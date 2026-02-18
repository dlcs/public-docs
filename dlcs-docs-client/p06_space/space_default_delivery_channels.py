import settings
from iiif_cs import get_cloud_services_resource, pprint, post_resource, delete_resource
from p06_space.get_put_patch_delete_space import get_space


def get_space_default_delivery_channels():
    space = get_space()
    default_delivery_channels = get_cloud_services_resource(space['defaultDeliveryChannels']).json()
    print("GET defaultDeliveryChannels returned")
    pprint(default_delivery_channels)
    print()
    return default_delivery_channels


def post_space_default_delivery_channel(resource_url):
    default_delivery_channel = {
        "channel": "iiif-av",
        "policy": f"{settings.IIIF_CS_API_HOST}/customers/{settings.IIIF_CS_CUSTOMER_ID}/deliveryChannelPolicies/iiif-av/default-video",
        "mediaType": "application/mp4"
    }
    r = post_resource(resource_url, default_delivery_channel)
    print("POST returned:")
    new_dc = r.json()
    pprint(new_dc)
    print()
    return new_dc


if __name__ == '__main__':
    space_dds = get_space_default_delivery_channels()
    delivery_channel = post_space_default_delivery_channel(space_dds['@id'])
    get_space_default_delivery_channels()
    delete_resource(delivery_channel['@id'])