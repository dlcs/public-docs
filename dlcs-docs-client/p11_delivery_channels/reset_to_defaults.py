import settings
from iiif_cs import patch_resource, get_cloud_services_resource, pprint
from settings import docs_space_id

# Asset registered with "none" channel in none_channel.py
asset_id = "none-channel-example"


def reset_delivery_channels_to_defaults(asset_id=asset_id, space_id=docs_space_id):
    """Reset an asset's delivery channels to defaults by PATCHing with the
    special 'default' channel. The platform will populate delivery channels
    from the Space or Customer defaultDeliveryChannels."""
    asset_path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}"

    patch = {
        "deliveryChannels": [
            {
                "@type": "vocab:DeliveryChannel",
                "channel": "default",
                "policy": "default"
            }
        ]
    }

    r = patch_resource(asset_path, patch)
    print("PATCH asset returned:")
    asset = r.json()
    pprint(asset)
    print()
    print(f"Asset deliveryChannels after reset: {asset.get('deliveryChannels')}")


if __name__ == '__main__':
    reset_delivery_channels_to_defaults()
