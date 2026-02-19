import settings
from iiif_cs import post_resource, get_cloud_services_resource, pprint
from p06_space.ensure_space import ensure_space
from settings import docs_space_id, docs_space_name


def register_asset_with_no_delivery_channels():
    """Register an asset with the 'none' delivery channel, meaning it will
    be stored in the platform but not served on any channel."""
    ensure_space(docs_space_id, docs_space_name)

    collection = {
        "member": [
            {
                "id": "none-channel-example",
                "space": docs_space_id,
                "mediaType": "image/jpeg",
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/by-the-rhine.jpg",
                "deliveryChannels": [
                    {
                        "@type": "vocab:DeliveryChannel",
                        "channel": "none",
                        "policy": "none"
                    }
                ]
            }
        ]
    }

    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue"
    r = post_resource(path, collection)
    print("POST to queue returned:")
    batch = r.json()
    pprint(batch)
    print()

    # Fetch the asset to confirm it has no delivery channels
    asset_path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{docs_space_id}/images/none-channel-example"
    asset = get_cloud_services_resource(asset_path).json()
    print("GET asset returned:")
    pprint(asset)
    print()
    print(f"Asset deliveryChannels: {asset.get('deliveryChannels')}")


if __name__ == '__main__':
    register_asset_with_no_delivery_channels()
