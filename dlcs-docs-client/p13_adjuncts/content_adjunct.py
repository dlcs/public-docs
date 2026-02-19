import requests
import settings
from settings import docs_space_id
from iiif_cs import (
    BASIC_AUTH_HEADER, get_cloud_services_resource,
    post_resource, put_resource, delete_resource, wait_for_value, pprint, normalise_path
)
from p07_asset.asset_adjuncts import ensure_rusty_boat_asset, rusty_boat_asset_id

# A file to fetch and supply as the adjunct content
content_source_url = "https://dlcs.github.io/public-docs/doc_fixtures/adjuncts/rusty-boat.txt"

adjunct_id = "content-description.txt"


def post_empty_adjunct(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """POST to create an adjunct with no origin and no content. The adjunct API
    resource is created immediately (201 Created), but has no publicId and size 0
    until binary content is supplied via a separate POST to the content sub-resource."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}/adjuncts"
    adjunct = {
        "id": adjunct_id,
        "@type": "Text",
        "mediaType": "text/plain",
        "label": {"en": ["Description of the rusty boat image"]},
        "iiifLink": "seeAlso"
    }
    r = post_resource(path, adjunct)
    print("POST adjunct (no content) returned:")
    created = r.json()
    pprint(created)
    print()
    return created


def post_content(adjunct, content_bytes, content_type="text/plain"):
    """POST the binary content to the adjunct's content sub-resource. This is a
    synchronous call but ingesting may briefly be true while the content is stored.
    The Content-Type header should match the adjunct's mediaType."""
    content_url = adjunct["content"]
    np = normalise_path(content_url)
    headers = {**BASIC_AUTH_HEADER, "Content-Type": content_type}
    print("-------------------------------------------")
    print(f"POST {np}")
    print(f"<binary body: {len(content_bytes)} bytes>")
    r = requests.post(np, headers=headers, data=content_bytes)
    print(f"HTTP Status Code: {r.status_code}")
    print()
    return r


def get_adjunct(adjunct_id=adjunct_id, asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """GET a single adjunct by its path."""
    path = (
        f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}"
        f"/images/{asset_id}/adjuncts/{adjunct_id}"
    )
    r = get_cloud_services_resource(path)
    print("GET adjunct returned:")
    pprint(r.json())
    print()
    return path


def delete_adjunct(adjunct_id=adjunct_id, asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """DELETE an adjunct."""
    path = (
        f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}"
        f"/images/{asset_id}/adjuncts/{adjunct_id}"
    )
    r = delete_resource(path)
    print(f"DELETE adjunct returned status: {r.status_code}")
    print()


if __name__ == '__main__':
    # NOTE: Adjunct support is not yet fully implemented.
    # The code below demonstrates the expected API operations.

    ensure_rusty_boat_asset()

    # Create the adjunct resource with no content - returns 201 with size=0 and no publicId
    adjunct = post_empty_adjunct()

    # GET to confirm: size is 0, no publicId, content URL is present
    adjunct_path = get_adjunct()

    # Fetch the bytes we want to store as the adjunct's content
    content_bytes = requests.get(content_source_url).content

    # POST the binary content to the adjunct's content sub-resource
    post_content(adjunct, content_bytes, content_type="text/plain")

    # Poll until ingesting is false - content has been stored and size measured
    wait_for_value(path=adjunct_path, field="ingesting", value=False, interval=2, retries=10)

    # GET to verify - publicId is now populated and size reflects actual byte count
    get_adjunct()

    # Clean up
    delete_adjunct()
