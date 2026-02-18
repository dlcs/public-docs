import settings
from iiif_cs import get_cloud_services_resource, pprint, patch_resource
from p06_space.get_put_patch_delete_space import get_space


# TODO: does not work! Is 404
def get_all_roles():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/roles"
    r = get_cloud_services_resource(path)
    print("GET returned:")
    roles = r.json()
    pprint(roles)
    return roles


def apply_default_roles():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{settings.docs_space_id}"
    space = {
        "defaultRoles": [
            f"{settings.IIIF_CS_API_HOST}/customers/{settings.IIIF_CS_CUSTOMER_ID}/roles/clickthrough"
        ]
    }
    r = patch_resource(path, space)
    pprint(r.json())
    print()


def clear_default_roles():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{settings.docs_space_id}"
    space = {
        "defaultRoles": []
    }
    r = patch_resource(path, space)
    pprint(r.json())
    print()


if __name__ == '__main__':
    # all_roles = get_all_roles()
    apply_default_roles()
    get_space()
    clear_default_roles()
    get_space()