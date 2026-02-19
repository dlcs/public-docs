import settings
from iiif_cs import get_cloud_services_resource, post_resource, put_resource, delete_resource, pprint


def setup_origin_strategy():
    """Create a CustomerOriginStrategy to use in this example."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/originStrategies"
    origin_strategy = {
        "strategy": "basic-http-authentication",
        "regex": "https\\:\\/\\/credentials-example\\.com\\/.*",
        "credentials": '{ \"user\": \"original-user\", \"password\": \"original-password\" }',
        "optimised": False,
        "order": 1
    }
    r = post_resource(path, origin_strategy)
    result = r.json()
    print("Created CustomerOriginStrategy:")
    pprint(result)
    print()
    return result


def update_credentials(origin_strategy_url):
    """PUT to the credentials sub-resource to update stored credentials.
    The request body is an escaped JSON string, not a JSON object."""
    credentials_url = origin_strategy_url + "/credentials"
    new_credentials = '{ "user": "updated-user", "password": "updated-password" }'
    r = put_resource(credentials_url, new_credentials)
    print("PUT credentials returned:")
    print(f"HTTP Status Code: {r.status_code}")
    print()


def delete_credentials(origin_strategy_url):
    """DELETE the stored credentials from a CustomerOriginStrategy."""
    credentials_url = origin_strategy_url + "/credentials"
    delete_resource(credentials_url)


if __name__ == '__main__':
    origin_strategy = setup_origin_strategy()
    origin_strategy_url = origin_strategy["@id"]

    # Update credentials - note: no GET is available, credentials always show as "xxx"
    update_credentials(origin_strategy_url)

    # GET the strategy to confirm it still works (credentials still shown as "xxx")
    r = get_cloud_services_resource(origin_strategy_url)
    print("GET after credentials update:")
    pprint(r.json())
    print()

    # DELETE the credentials
    delete_credentials(origin_strategy_url)

    # Clean up
    delete_resource(origin_strategy_url)
