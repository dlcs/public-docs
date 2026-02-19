import settings
from iiif_cs import get_cloud_services_resource, post_resource, put_resource, delete_resource, pprint


def post_origin_strategy():
    """POST to create a new CustomerOriginStrategy. The platform assigns a unique GUID
    path element - you cannot create one with PUT."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/originStrategies"
    origin_strategy = {
        "strategy": "basic-http-authentication",
        "regex": "https\\:\\/\\/example\\.com\\/images\\/.*",
        "credentials": '{ \"user\": \"uuu\", \"password\": \"ppp\" }',
        "optimised": False,
        "order": 1
    }
    r = post_resource(path, origin_strategy)
    print("POST CustomerOriginStrategy returned:")
    result = r.json()
    pprint(result)
    print()
    return result


def get_origin_strategy(origin_strategy_id):
    """GET a CustomerOriginStrategy by its URL. Note that credentials are never
    returned by the API - they always appear as 'xxx'."""
    r = get_cloud_services_resource(origin_strategy_id)
    print("GET CustomerOriginStrategy returned:")
    pprint(r.json())
    print()
    return r


def put_origin_strategy(origin_strategy_id):
    """PUT to update an existing CustomerOriginStrategy. Can update regex, strategy,
    optimised and order. Credentials must be supplied for strategies that require them,
    but supplying them here does not update the stored credentials."""
    origin_strategy = {
        "strategy": "basic-http-authentication",
        "regex": "https\\:\\/\\/example\\.com\\/images\\/.*",
        "credentials": '{ \"user\": \"uuu\", \"password\": \"ppp\" }',
        "optimised": False,
        "order": 2
    }
    r = put_resource(origin_strategy_id, origin_strategy)
    print("PUT CustomerOriginStrategy returned:")
    pprint(r.json())
    print()
    return r


def delete_origin_strategy(origin_strategy_id):
    """DELETE a CustomerOriginStrategy."""
    delete_resource(origin_strategy_id)


if __name__ == '__main__':
    # Expected: POST 201 Created
    origin_strategy = post_origin_strategy()
    origin_strategy_id = origin_strategy["@id"]

    # Expected: GET 200 OK
    get_origin_strategy(origin_strategy_id)

    # Expected: PUT 200 OK (update order)
    put_origin_strategy(origin_strategy_id)

    # Expected: GET 200 OK (verify update)
    get_origin_strategy(origin_strategy_id)

    # Expected: DELETE 204 No Content
    delete_origin_strategy(origin_strategy_id)

    # Expected: GET 404 Not Found
    get_origin_strategy(origin_strategy_id)
