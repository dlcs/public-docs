import settings
from iiif_cs import get_cloud_services_resource, pprint


def get_queue_images():
    """GET the collection of assets currently on the queue, across all batches."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/queue/images"
    r = get_cloud_services_resource(path)
    print("GET Queue Images returned:")
    if r.status_code == 200:
        images = r.json()
        pprint(images)
    else:
        print(f"Status {r.status_code} - queue may be empty")
        images = None
    print()
    return images


if __name__ == '__main__':
    get_queue_images()
