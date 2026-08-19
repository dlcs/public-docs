import settings
from iiif_cs import get_cloud_services_resource, post_resource, delete_resource, pprint

# The same named query can be projected into different output types by changing
# the {output-type} path element of the public URL:
#     https://dlcs.example/{output-type}/{customer-name}/{query-name}/{p1}/{p2}/...
# This sample projects one named query as raw-resource, zip and pdf.

named_query_name = "docs-example-outputs"

# The public-facing host is the API host without the "api." prefix
public_host = settings.IIIF_CS_API_HOST.replace("//api.", "//", 1)

# Parameter values for the template "assetOrder=n1&space=p1&s1=p2" - these select the
# assets set up by named_queries_examples.py
p1_p2 = f"{settings.named_query_space_id}/autumn-1985"


def post_named_query():
    """Create the named query this sample projects. The objectname parameter applies
    only to the stored (pdf and zip) projections: it names the stored object, using
    replacement tokens like {s1} that are substituted with metadata values from the
    query. Without it, stored objects are named 'Untitled'."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/namedQueries"
    named_query = {
        "name": named_query_name,
        "template": "assetOrder=n1&space=p1&s1=p2&objectname={s1}.zip"
    }
    r = post_resource(path, named_query)
    print("POST NamedQuery returned:")
    nq = r.json()
    pprint(nq)
    print()
    return nq


def public_url(output_type):
    return f"{public_host}/{output_type}/{settings.IIIF_CS_CUSTOMER_NAME}/{named_query_name}/{p1_p2}"


def get_raw_resource():
    """raw-resource returns a plain JSON array of the identifiers of the assets
    the query selects, in query order."""
    r = get_cloud_services_resource(public_url("raw-resource"))
    print("raw-resource projection:")
    pprint(r.json())
    print()


def get_zip():
    """The zip projection is generated and stored on first request. It contains a
    thumbnail of each selected image asset (the size closest to the platform's
    configured projection size, 1000px by default), not the original files.
    A 202 response with a Retry-After header means generation is still in progress."""
    r = get_cloud_services_resource(public_url("zip"))
    if r.status_code == 202:
        print(f"zip is being generated - retry after {r.headers.get('Retry-After')} seconds")
    else:
        print(f"zip projection: {r.headers.get('Content-Type')}, {len(r.content)} bytes")
    print()


def get_control_file(output_type):
    """Each stored projection has a control file describing its state - 'exists' means
    the generated resource is stored, 'inProcess' means generation is under way.
    The 'key' ends with the objectname from the template - here 'autumn-1985.zip',
    from objectname={s1}.zip."""
    r = get_cloud_services_resource(public_url(f"{output_type}-control"))
    print(f"{output_type}-control file:")
    pprint(r.json())
    print()


def get_pdf():
    """The pdf projection behaves like zip, but PDF generation depends on a separate
    service and may not be enabled on all environments. Where it is not available,
    requests keep returning 202 and the control file keeps reporting inProcess."""
    r = get_cloud_services_resource(public_url("pdf"))
    if r.status_code == 202:
        print(f"pdf is being generated - retry after {r.headers.get('Retry-After')} seconds")
        print("(if this never completes, PDF generation may not be enabled on this environment)")
    elif r.status_code == 200:
        print(f"pdf projection: {r.headers.get('Content-Type')}, {len(r.content)} bytes")
    else:
        print(f"pdf projection returned status: {r.status_code}")
    print()


def purge_pdf():
    """A generated PDF (and its control file) can be purged through the platform API,
    so that the next request regenerates it. There is no equivalent for zip."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/resources/pdf/{named_query_name}?args={p1_p2}"
    r = delete_resource(path)
    print(f"DELETE pdf resource returned: {r.json()}")
    print()


def delete_named_query(id):
    """DELETE the named query created for this sample."""
    r = delete_resource(id)
    print(f"DELETE NamedQuery returned status: {r.status_code}")
    print()


if __name__ == '__main__':
    # Expected: POST 201 Created
    new_nq = post_named_query()

    # Expected: 200 OK, a JSON array of asset identifiers
    get_raw_resource()

    # Expected: 200 OK application/zip (or 202 while generating - run again)
    get_zip()

    # Expected: 200 OK, exists true once generated
    get_control_file("zip")

    # Expected: 202 while generating; 200 application/pdf once generated -
    # or 202 indefinitely where PDF generation is not enabled
    get_pdf()
    get_control_file("pdf")

    # Expected: 200 OK with a {"success": true} body
    purge_pdf()

    # Expected: DELETE 204 No Content
    delete_named_query(new_nq['@id'])
