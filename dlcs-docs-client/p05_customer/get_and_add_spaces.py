import settings
from iiif_cs import get_cloud_services_resource, post_resource, pprint


def get_spaces():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces"
    spaces = get_cloud_services_resource(path).json()
    print("GET returned:")
    pprint(spaces)
    print()

# TODO: This does not use supplied id. Should be... 409? on POST? Or Bad Request, no id should be passed?
# def post_space_id_exists():
#     # what happens if we POST an existing space?
#     space = {
#         "id": 1, # Already exists!
#         "name": "Conflicting space"
#     }
#     path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces"
#     new_space = post_resource(path, space).json()
#     print("POST returned:")
#     pprint(new_space)
#     print()


# TODO: This does not use supplied id. Should be... Bad Request, no id should be passed?
# def post_space_id_new():
#     # what happens if we POST an existing space?
#     space = {
#         "id": 2999, # Doesn't exist
#         "name": "Space 2999"
#     }
#     path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces"
#     new_space = post_resource(path, space).json()
#     print("POST returned:")
#     pprint(new_space)
#     print()


# NB you'll need to modify these if you run more than once
def create_space():
    space = {
        "name": "A new space created now"
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces"
    new_space = post_resource(path, space).json()
    print("POST returned:")
    pprint(new_space)
    print()


if __name__ == '__main__':
    get_spaces()
    create_space()