import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, post_resource, delete_resource, pprint

# Asset ID from p02_registering/put.py
rusty_boat_asset_id = "put-example-1-rusty-boat"

# Example adjunct origin
adjunct_origin = "https://dlcs.github.io/public-docs/doc_fixtures/adjuncts/rusty-boat.txt"


def ensure_rusty_boat_asset():
    """Ensure the rusty boat asset exists, create it if not."""
    asset_path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{docs_space_id}/images/{rusty_boat_asset_id}"
    r = get_cloud_services_resource(asset_path)
    if r.status_code == 404:
        print(f"Asset {rusty_boat_asset_id} does not exist. Creating it...")
        from p02_registering.put import put_asset
        put_asset()
    return asset_path


def get_adjuncts(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """List all adjuncts for an asset."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}/adjuncts"
    r = get_cloud_services_resource(path)
    print("GET adjuncts returned:")
    adjuncts = r.json()
    pprint(adjuncts)
    print()
    return adjuncts


def post_adjunct(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """Add a new adjunct to an asset by supplying an origin."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}/adjuncts"
    adjunct = {
        "id": "rusty-boat-description.txt",
        "origin": adjunct_origin,
        "@type": "Text",
        "mediaType": "text/plain",
        "label": {"en": ["Description of the rusty boat image"]},
        "iiifLink": "seeAlso"
    }
    r = post_resource(path, adjunct)
    print("POST adjunct returned:")
    created_adjunct = r.json()
    pprint(created_adjunct)
    print()
    return created_adjunct


def delete_adjunct(adjunct_id="rusty-boat-description.txt", asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """Delete an adjunct from an asset."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}/adjuncts/{adjunct_id}"
    r = delete_resource(path)
    print(f"DELETE adjunct returned status: {r.status_code}")
    print()
    return r


if __name__ == '__main__':
    # NOTE: This feature is not yet implemented.
    # The code below demonstrates the expected API operations.

    # Ensure the rusty boat asset exists
    ensure_rusty_boat_asset()

    # List adjuncts (should be empty initially)
    get_adjuncts()

    # Add an adjunct
    post_adjunct()

    # List adjuncts again (should now contain one)
    get_adjuncts()

    # Delete the adjunct
    delete_adjunct()

    # List adjuncts again (should be empty again)
    get_adjuncts()
