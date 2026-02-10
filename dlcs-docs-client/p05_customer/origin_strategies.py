import settings
from iiif_cs import get_cloud_services_resource, post_resource, pprint


def get_origin_strategies():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/originStrategies"
    origin_strategies = get_cloud_services_resource(path).json()
    print("GET returned:")
    pprint(origin_strategies)
    print()


def post_system_origin_strategy():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/originStrategies"
    basic_auth_for_my_site = {
        "regex": "https\\:\\/\\/example\\.com\\/images\\/.*(?<!\\.tif|\\.tiff)$",
        # "strategy": f"https://{settings.IIIF_CS_API_HOST}/originStrategies/basic-http-authentication",
        "strategy": "basic-http-authentication",
        "credentials": '{ \"user\": \"uuu\", \"password\": \"ppp\" }',
        "optimised": False,
        "order": 1
    }
    r = post_resource(path, basic_auth_for_my_site)
    print("POST returned:")
    pprint(r.json())
    print()


if __name__ == '__main__':
    get_origin_strategies()
    post_system_origin_strategy()