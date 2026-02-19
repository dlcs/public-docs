import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, post_resource, delete_resource, pprint
from p07_asset.asset_adjuncts import ensure_rusty_boat_asset, rusty_boat_asset_id


def post_multiple_adjuncts(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """POST an array of adjuncts in a single request. The platform creates all of
    them and begins fetching content from their origins concurrently. Each will
    have ingesting=true until its content has been stored."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}/adjuncts"
    adjuncts = [
        {
            "id": "bulk-description.txt",
            "origin": "https://dlcs.github.io/public-docs/doc_fixtures/adjuncts/rusty-boat.txt",
            "@type": "Text",
            "mediaType": "text/plain",
            "label": {"en": ["Plain text description"]},
            "iiifLink": "seeAlso",
            "language": ["en"]
        },
        {
            "id": "bulk-description-2.txt",
            "origin": "https://dlcs.github.io/public-docs/doc_fixtures/adjuncts/rusty-boat.txt",
            "@type": "Text",
            "mediaType": "text/plain",
            "label": {"en": ["A second plain text description"]},
            "iiifLink": "rendering",
            "language": ["en"]
        }
    ]
    r = post_resource(path, adjuncts)
    print("POST multiple adjuncts returned:")
    result = r.json()
    pprint(result)
    print()
    return result


def get_adjuncts(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """GET the adjuncts collection for an asset to list all adjuncts."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}/adjuncts"
    r = get_cloud_services_resource(path)
    print("GET adjuncts returned:")
    pprint(r.json())
    print()


def delete_adjunct(adjunct_id, asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """DELETE a single adjunct by id."""
    path = (
        f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}"
        f"/images/{asset_id}/adjuncts/{adjunct_id}"
    )
    r = delete_resource(path)
    print(f"DELETE {adjunct_id} returned status: {r.status_code}")
    print()


if __name__ == '__main__':
    # NOTE: Adjunct support is not yet fully implemented.
    # The code below demonstrates the expected API operations.

    ensure_rusty_boat_asset()

    # POST an array of adjuncts in one request
    post_multiple_adjuncts()

    # GET the collection to see all adjuncts on the asset
    get_adjuncts()

    # Clean up
    delete_adjunct("bulk-description.txt")
    delete_adjunct("bulk-description-2.txt")
