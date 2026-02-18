from iiif_cs import get_cloud_services_resource, pprint, post_resource, delete_resource
from p06_space.get_put_patch_delete_space import get_space

# TODO: not implemented
def get_space_metadata():
    space = get_space()
    metadata = get_cloud_services_resource(space['metadata']).json()
    print("GET metadata returned")
    pprint(metadata)
    print()
    return metadata


if __name__ == '__main__':
    space_md = get_space_metadata()