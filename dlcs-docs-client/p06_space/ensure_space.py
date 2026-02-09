import settings
from iiif_cs import get_cloud_services_resource, put_resource


# Usually you know whether the space exists already, but for these examples we'll
# have this helper that makes sure it exists.
def ensure_space(space_id: int, name: str):
    space_path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}"
    r1 = get_cloud_services_resource(space_path)
    if r1.status_code == 404:
        print(f"{space_path} does not exist, will create it")
        put_resource(space_path, {"name": name})
        r1 = get_cloud_services_resource(space_path)
    return r1.json()
