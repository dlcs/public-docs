import settings
from iiif_cs import get_cloud_services_resource, post_resource, put_resource, delete_resource, pprint

# A unique name for this example named query - becomes the last path element of its @id
# and appears in the public-facing URL
named_query_name = "docs-example-manifest"


def post_named_query():
    """POST to the namedQueries collection to create a new named query. The platform
    uses the 'name' field as the last path element - you cannot create a named query
    with PUT. The template selects assets by string1 (p1) in a given space (p2),
    ordered by number1."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/namedQueries"
    named_query = {
        "name": named_query_name,
        "template": "manifest=s1&canvas=n1&spacename=p1&s1=p2"
    }
    r = post_resource(path, named_query)
    print("POST NamedQuery returned:")
    nq = r.json()
    pprint(nq)
    print()
    return nq


def get_named_query(id):
    """GET a named query by its URI."""
    r = get_cloud_services_resource(id)
    print("GET NamedQuery returned:")
    pprint(r.json())
    print()


def put_named_query(id):
    """PUT to update an existing named query. Only the template can be updated this way -
    you cannot change the name via PUT. Delete and re-create if you need a new name."""
    named_query = {
        "template": "manifest=s1&canvas=n1&space=p1&s1=p2"
    }
    r = put_resource(id, named_query)
    print("PUT NamedQuery returned:")
    pprint(r.json())
    print()


def delete_named_query(id):
    """DELETE a named query."""
    r = delete_resource(id)
    print(f"DELETE NamedQuery returned status: {r.status_code}")
    print()


def show_public_url(customer_name, space_id, string1_value):
    """The named query is invoked via a public-facing URL on a different host,
    not via the API. The URL pattern is:
        https://dlcs.example/iiif-resource/{customer-name}/{query-name}/{p1}/{p2}/...

    For this template ('manifest=s1&canvas=n1&space=p1&s1=p2') with two
    parameters, the public URL would look like this:"""
    # Not a very elegant way of doing this:
    public_host = settings.IIIF_CS_API_HOST.replace("/api.", "/", count=1)
    url = f"{public_host}/iiif-resource/{customer_name}/{named_query_name}/{space_id}/{string1_value}"
    print("Public-facing named query URL (no API credentials required):")
    print(url)
    print()
    return url


def get_public_url(url):
    r = get_cloud_services_resource(url)
    print("GET Public URL:")
    pprint(r.json())
    print()


if __name__ == '__main__':
#     delete_resource("https://api.dlcs-stage.digirati.io/customers/15/namedQueries/ea098e98-03b0-477b-b73a-ea8e427ac923")
# else:
    # Expected: POST 201 Created
    new_nq = post_named_query()

    # Expected: GET 200 OK
    get_named_query(new_nq['@id'])

    # Expected: PUT 200 OK (update template to use spacename instead of space id)
    put_named_query(new_nq['@id'])

    # Expected: GET 200 OK (confirm updated template)
    get_named_query(new_nq['@id'])

    # Show what the public-facing invocation URL looks like
    url = show_public_url(customer_name=settings.IIIF_CS_CUSTOMER_NAME, space_id=settings.docs_space_id, string1_value="catalogue-1985")

    # Show the generated named query manifest
    get_public_url(url)

    # Expected: DELETE 204 No Content
    # delete_named_query(new_nq['@id'])

    # Expected: GET 404 Not Found
    get_named_query(new_nq['@id'])
