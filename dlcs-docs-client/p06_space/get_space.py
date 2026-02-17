import settings
from settings import docs_space_id, temp_space_id
from iiif_cs import get_cloud_services_resource, put_resource, delete_resource, pprint
from p05_customer.get_and_add_spaces import get_spaces


def get_space(space_id=docs_space_id):
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}"
    space = get_cloud_services_resource(path).json()
    print("GET Space returned")
    pprint(space)
    print()
    return space


def put_new_space():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{temp_space_id}"
    space = {
        "name": "pi space",
        "defaultTags": [ "green", "red" ]
    }
    r = put_resource(path, space)
    pprint(r.json())
    print()


def put_existing_space():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{temp_space_id}"
    space = {
        "name": "pi space",
        "defaultTags": [ "green", "red" ]
    }
    r = put_resource(path, space)
    pprint(r.json())
    print()


# TODO: This should be a Bad Request? Instead it is accepted, 918273 is ignored.
def put_new_space_with_conflicting_id():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{temp_space_id}"
    space = {
        "id": 918273,
        "name": "put conflict space",
        "defaultTags": [ "green", "red" ]
    }
    r = put_resource(path, space)
    pprint(r.json())
    print()


def delete_space():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{temp_space_id}"
    delete_resource(path)


if __name__ == '__main__':
    get_space()
    put_new_space()
    get_spaces()
    put_existing_space()
    delete_space()
    get_spaces()
    # put_new_space_with_conflicting_id()
    # get_spaces()