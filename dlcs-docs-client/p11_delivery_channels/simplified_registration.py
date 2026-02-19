import settings
from iiif_cs import post_resource, pprint
from p06_space.ensure_space import ensure_space
from settings import docs_space_id, docs_space_name

origin = "https://dlcs.github.io/public-docs/doc_fixtures/by-the-rhine.jpg"


def register_with_full_delivery_channels():
    """Register an asset with delivery channels specified in full,
    including @type, channel and policy."""
    collection = {
        "member": [
            {
                "id": "simplified-dc-example-1",
                "space": docs_space_id,
                "mediaType": "image/jpeg",
                "origin": origin,
                "deliveryChannels": [
                    {
                        "@type": "vocab:DeliveryChannel",
                        "channel": "iiif-img",
                        "policy": "default"
                    },
                    {
                        "@type": "vocab:DeliveryChannel",
                        "channel": "thumbs",
                        "policy": f"{settings.IIIF_CS_API_HOST}/customers/{settings.IIIF_CS_CUSTOMER_ID}/deliveryChannelPolicies/thumbs/default"
                    }
                ]
            }
        ]
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue"
    r = post_resource(path, collection)
    batch = r.json()
    print("Full form - POST returned batch:")
    pprint(batch)
    print()


def register_without_type():
    """Register an asset with delivery channels omitting @type."""
    collection = {
        "member": [
            {
                "id": "simplified-dc-example-2",
                "space": docs_space_id,
                "mediaType": "image/jpeg",
                "origin": origin,
                "deliveryChannels": [
                    {
                        "channel": "iiif-img",
                        "policy": "default"
                    },
                    {
                        "channel": "thumbs",
                        "policy": f"{settings.IIIF_CS_API_HOST}/customers/{settings.IIIF_CS_CUSTOMER_ID}/deliveryChannelPolicies/thumbs/default"
                    }
                ]
            }
        ]
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue"
    r = post_resource(path, collection)
    batch = r.json()
    print("Without @type - POST returned batch:")
    pprint(batch)
    print()


def register_without_policy():
    """Register an asset specifying only channels, with policy resolved from defaults."""
    collection = {
        "member": [
            {
                "id": "simplified-dc-example-3",
                "space": docs_space_id,
                "mediaType": "image/jpeg",
                "origin": origin,
                "deliveryChannels": [
                    {"channel": "iiif-img"},
                    {"channel": "thumbs"}
                ]
            }
        ]
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue"
    r = post_resource(path, collection)
    batch = r.json()
    print("Without policy - POST returned batch:")
    pprint(batch)
    print()


def register_with_string_array():
    """Register an asset supplying delivery channels as a simple array of strings.
    Policy for each channel is resolved from defaults."""
    collection = {
        "member": [
            {
                "id": "simplified-dc-example-4",
                "space": docs_space_id,
                "mediaType": "image/jpeg",
                "origin": origin,
                "deliveryChannels": ["iiif-img", "thumbs"]
            }
        ]
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue"
    r = post_resource(path, collection)
    batch = r.json()
    print("String array form - POST returned batch:")
    pprint(batch)
    print()


def register_with_no_delivery_channels():
    """Register an asset with no delivery channels at all.
    The platform will match channels from Space or Customer defaults based on mediaType."""
    collection = {
        "member": [
            {
                "id": "simplified-dc-example-5",
                "space": docs_space_id,
                "mediaType": "image/jpeg",
                "origin": origin
            }
        ]
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue"
    r = post_resource(path, collection)
    batch = r.json()
    print("No delivery channels - POST returned batch:")
    pprint(batch)
    print()


if __name__ == '__main__':
    ensure_space(docs_space_id, docs_space_name)

    register_with_full_delivery_channels()
    register_without_type()
    register_without_policy()
    register_with_string_array()
    register_with_no_delivery_channels()
