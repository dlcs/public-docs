import json
import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, pprint


def get_images_by_shortcut_field(string1_value, space_id=docs_space_id):
    """Filter space images using the shortcut query parameter form.
    Only the 6 built-in fields (string1-3, number1-3) are supported."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images"
    query = f"?string1={string1_value}"
    r = get_cloud_services_resource(path + query)
    print(f"GET images with ?string1={string1_value} returned:")
    images = r.json()
    pprint(images)
    print(f"{len(images.get('member', []))} assets returned.")
    print()


def get_images_by_q_object(space_id=docs_space_id):
    """Filter space images using the q query parameter with a JSON object.
    Equivalent to the shortcut form but allows combining multiple fields."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images"
    q = json.dumps({"string1": "catalogue-1985", "number1": 1})
    query = f"?q={q}"
    r = get_cloud_services_resource(path + query)
    print(f"GET images with q={q} returned:")
    images = r.json()
    pprint(images)
    print(f"{len(images.get('member', []))} assets returned.")
    print()


def get_images_paginated(space_id=docs_space_id):
    """Retrieve a page of results using pageSize and page parameters.
    If no page is specified, the first page is returned."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images"
    query = "?pageSize=10&page=1"
    r = get_cloud_services_resource(path + query)
    print("GET images with pageSize=10&page=1 returned:")
    images = r.json()
    pprint(images)
    print(f"{len(images.get('member', []))} assets returned.")
    print()


def get_all_images_by_shortcut_field(string1_value):
    """Query across all spaces using the customer-level allImages endpoint."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/allImages"
    query = f"?string1={string1_value}"
    r = get_cloud_services_resource(path + query)
    print(f"GET allImages with ?string1={string1_value} returned:")
    images = r.json()
    pprint(images)
    print(f"{len(images.get('member', []))} assets returned.")
    print()


# --- Not yet implemented ---

def get_images_by_tags(tags, space_id=docs_space_id):
    """Filter by tags. NOTE: Not yet supported - returns unfiltered results or an error."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images"
    q = json.dumps({"tags": tags})
    query = f"?q={q}"
    r = get_cloud_services_resource(path + query)
    print(f"GET images with tags={tags} returned:")
    images = r.json()
    pprint(images)
    print()


def get_images_by_roles(roles, space_id=docs_space_id):
    """Filter by roles. NOTE: Not yet supported - returns unfiltered results or an error."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images"
    q = json.dumps({"roles": roles})
    query = f"?q={q}"
    r = get_cloud_services_resource(path + query)
    print(f"GET images with roles={roles} returned:")
    images = r.json()
    pprint(images)
    print()


def get_images_by_id(asset_id, space_id=docs_space_id):
    """Filter by model id. NOTE: Not yet supported - returns unfiltered results or an error."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images"
    q = json.dumps({"id": asset_id})
    query = f"?q={q}"
    r = get_cloud_services_resource(path + query)
    print(f"GET images with id={asset_id} returned:")
    images = r.json()
    pprint(images)
    print()


def get_images_ordered(order_by_field, descending=False, space_id=docs_space_id):
    """Order results by a field. NOTE: Not yet supported - ordering is ignored."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images"
    param = "orderByDescending" if descending else "orderBy"
    query = f"?{param}={order_by_field}"
    r = get_cloud_services_resource(path + query)
    print(f"GET images with {param}={order_by_field} returned:")
    images = r.json()
    pprint(images)
    print(f"{len(images.get('member', []))} assets returned.")
    print()


def get_images_by_multiple_values(field, values, space_id=docs_space_id):
    """Filter where a field matches any of the supplied values (OR).
    NOTE: Not yet supported - returns unfiltered results or an error."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images"
    q = json.dumps({field: values})
    query = f"?q={q}"
    r = get_cloud_services_resource(path + query)
    print(f"GET images with {field}={values} (OR) returned:")
    images = r.json()
    pprint(images)
    print()


if __name__ == '__main__':
    # Implemented - shortcut field form
    get_images_by_shortcut_field("catalogue-1985")

    # Implemented - q object with combined fields
    get_images_by_q_object()

    # Implemented - pagination
    get_images_paginated()

    # Implemented - query across all spaces
    get_all_images_by_shortcut_field("catalogue-1985")

    # Not yet implemented - these demonstrate expected behaviour when supported
    get_images_by_tags(["my-tag"])
    get_images_by_roles([f"https://api.dlcs.example/customers/{settings.IIIF_CS_CUSTOMER_ID}/roles/clickthrough"])
    get_images_by_id("PHOTO.2.22.36.2.tif")
    get_images_ordered("width", descending=True)
    get_images_by_multiple_values("string1", ["value-a", "value-b"])
