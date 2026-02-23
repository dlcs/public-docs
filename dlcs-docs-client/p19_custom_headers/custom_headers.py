import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, post_resource, put_resource, delete_resource, pprint


def create_space_scoped_header(space_id=docs_space_id):
    """POST a new custom header scoped to a specific space.

    The platform assigns a GUID as the identifier; creation is always via POST
    to the collection, not PUT to a chosen URL.
    """
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/customHeaders"
    header = {
        "key": "Cache-Control",
        "value": "public, s-maxage=86400, max-age=86400",
        "space": space_id
    }
    r = post_resource(path, header)
    print("POST (space-scoped) returned:")
    created = r.json()
    pprint(created)
    print()
    return created


def create_role_scoped_header():
    """POST a custom header scoped to a role.

    The role URI follows the pattern: {api-host}/customers/{customer}/roles/{roleId}
    """
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/customHeaders"
    role_uri = f"{settings.IIIF_CS_API_HOST}/customers/{settings.IIIF_CS_CUSTOMER_ID}/roles/clickthrough"
    header = {
        "key": "Cache-Control",
        "value": "private, max-age=600",
        "role": role_uri
    }
    r = post_resource(path, header)
    print("POST (role-scoped) returned:")
    created = r.json()
    pprint(created)
    print()
    return created


def get_custom_header(header):
    """GET a single CustomHeader resource by its @id."""
    r = get_cloud_services_resource(header["@id"])
    print("GET returned:")
    pprint(r.json())
    print()


def update_custom_header(header):
    """PUT to update an existing custom header.

    The request body contains only the content fields (key, value, space, role).
    Do not include @id, @type or @context — the API will reject the request if
    @id is present in the body.
    """
    updated = {"key": header["key"], "value": "public, s-maxage=2419200, max-age=2419200"}
    if "space" in header:
        updated["space"] = header["space"]
    if "role" in header:
        updated["role"] = header["role"]
    r = put_resource(header["@id"], updated)
    print("PUT returned:")
    pprint(r.json())
    print()
    return r.json()


if __name__ == '__main__':
    # Create a header that applies to all assets in a specific space
    space_header = create_space_scoped_header()

    # GET the individual resource by its @id
    get_custom_header(space_header)

    # PUT to change the header value
    update_custom_header(space_header)

    # Create a second header scoped to a role (no space restriction)
    role_header = create_role_scoped_header()

    # Clean up both test headers
    delete_resource(space_header["@id"])
    delete_resource(role_header["@id"])
    print("Deleted test headers.")
