import settings
from iiif_cs import get_cloud_services_resource, post_resource, pprint


def get_default_delivery_channels():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/defaultDeliveryChannels"
    default_delivery_channels = get_cloud_services_resource(path).json()
    print("GET returned:")
    pprint(default_delivery_channels)
    print()


def post_default_delivery_channel():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/defaultDeliveryChannels"
    default_delivery_channel = {
        "channel": "iiif-av",
        "policy": f"{settings.IIIF_CS_API_HOST}/customers/{settings.IIIF_CS_CUSTOMER_ID}/deliveryChannelPolicies/iiif-av/default-video",
        "mediaType": "application/mp4"
    }
    r = post_resource(path, default_delivery_channel)
    print("POST returned:")
    pprint(r.json())
    print()


if __name__ == '__main__':
    get_default_delivery_channels()
    post_default_delivery_channel()