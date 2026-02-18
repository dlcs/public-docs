from iiif_cs import get_cloud_services_resource, pprint, post_resource, delete_resource
from p06_space.get_put_patch_delete_space import get_space


def get_space_storage():
    space = get_space()
    storage = get_cloud_services_resource(space['storage']).json()
    print("GET storage returned")
    pprint(storage)
    print()
    return storage


if __name__ == '__main__':
    space_md = get_space_storage()