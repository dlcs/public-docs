import settings
from iiif_cs import get_cloud_services_resource, post_resource, pprint


def get_custom_headers():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/customHeaders"
    custom_headers = get_cloud_services_resource(path).json()
    print("GET returned:")
    pprint(custom_headers)
    print()


def post_custom_header():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/customHeaders"
    custom_header = {
        "key": "Cache-Control",
        "value": "public, s-maxage=2419200, max-age=2419200",
        "space": 1
    }
    r = post_resource(path, custom_header)
    print("POST returned:")
    pprint(r.json())
    print()


if __name__ == '__main__':
    get_custom_headers()
    post_custom_header()