import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, post_resource, put_resource, delete_resource, wait_for_value, pprint
from p07_asset.asset_adjuncts import ensure_rusty_boat_asset, rusty_boat_asset_id

# A publicly accessible file for the platform to fetch and store
adjunct_origin = "https://dlcs.github.io/public-docs/doc_fixtures/adjuncts/rusty-boat.txt"

adjunct_id = "origin-description.txt"


def post_origin_adjunct(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """POST to create an adjunct from an origin. The platform fetches the content
    from the origin and stores it. The response is 201 Created immediately, but
    the 'ingesting' property will be true until the content has been stored."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}/adjuncts"
    adjunct = {
        "id": adjunct_id,
        "origin": adjunct_origin,
        "@type": "Text",
        "mediaType": "text/plain",
        "label": {"en": ["Description of the rusty boat image"]},
        "iiifLink": "seeAlso",
        "language": ["en"]
    }
    r = post_resource(path, adjunct)
    print("POST origin adjunct returned:")
    created = r.json()
    pprint(created)
    print()
    return created


def put_origin_adjunct(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """PUT to create (or update) an origin adjunct directly at its path. The id
    is taken from the URL path element, so it is optional in the body."""
    path = (
        f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}"
        f"/images/{asset_id}/adjuncts/{adjunct_id}"
    )
    adjunct = {
        "origin": adjunct_origin,
        "@type": "Text",
        "mediaType": "text/plain",
        "label": {"en": ["Description of the rusty boat image (via PUT)"]},
        "iiifLink": "seeAlso",
        "language": ["en"]
    }
    r = put_resource(path, adjunct)
    print("PUT origin adjunct returned:")
    pprint(r.json())
    print()


def get_adjunct(adjunct_id=adjunct_id, asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """GET a single adjunct by its path. When ingesting is false, publicId and
    content will be populated and size will reflect the actual stored byte count."""
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

    # Create an origin adjunct via POST - returns 201 immediately, ingesting=true
    post_origin_adjunct()

    # Poll until ingesting is false - content has been fetched and stored
    adjunct_path = (
        f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{docs_space_id}"
        f"/images/{rusty_boat_asset_id}/adjuncts/{adjunct_id}"
    )
    wait_for_value(path=adjunct_path, field="ingesting", value=False, interval=2, retries=10)

    # GET to verify - publicId, content and size are now populated
    get_adjunct()

    # Clean up
    delete_adjunct()
