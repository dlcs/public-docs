from get_images import get_images
from iiif_cs import delete_resource, get_cloud_services_resource, pprint
from p06_space.get_space import get_space


def purge_space(space_id: int):
    images_to_delete = get_images(space_id, ensure_space_exists=False)
    for image in images_to_delete['member']:
        delete_resource(image['@id'])


if __name__ == '__main__':
    danger_space_id = -1 # change this to the space you want to purge

    purge_space(danger_space_id)
    space = get_space(danger_space_id)
    images = get_cloud_services_resource(space['images']).json()
    pprint(images)

    # And delete the space itself:
    if len(images['member']) == 0:
        delete_resource(space['@id'])
    else:
        print("Run again to carry on deleting assets from the space")