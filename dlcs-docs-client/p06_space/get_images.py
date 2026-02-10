import settings
from iiif_cs import post_resource, pprint, get_cloud_services_resource
from p06_space.ensure_space import ensure_space


def get_images():
    space = 1
    ensure_space(space, "Space created by documentation example")
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space}/images"
    r = get_cloud_services_resource(path)
    print("GET returned:")
    images = r.json() # We expect this to be a batch
    pprint(images)
    print()



if __name__ == '__main__':
    get_images()