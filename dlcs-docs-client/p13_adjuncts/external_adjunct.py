import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, post_resource, put_resource, delete_resource, pprint
from p07_asset.asset_adjuncts import ensure_rusty_boat_asset, rusty_boat_asset_id

# An external URL for the adjunct - not fetched or stored by the platform
external_adjunct_url = (
    "https://dlcsstage-public-test-objects.s3.eu-west-1.amazonaws.com"
    "/images-with-text/b29820947_0014.jp2.xml"
)

adjunct_id = "external-alto.xml"


def post_external_adjunct(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """POST to create an adjunct that links to an external URL. The platform records the
    link but does not fetch or store the content. The publicId will be the externalId."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}/adjuncts"
    adjunct = {
        "id": adjunct_id,
        "externalId": external_adjunct_url,
        "@type": "Dataset",
        "mediaType": "text/xml",
        "profile": "http://www.loc.gov/standards/alto/v3/alto.xsd",
        "label": {"en": ["METS-ALTO XML (external)"]},
        "size": 36032,
        "iiifLink": "seeAlso",
        "language": ["en"]
    }
    r = post_resource(path, adjunct)
    print("POST external adjunct returned:")
    created = r.json()
    pprint(created)
    print()
    return created


def put_external_adjunct(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """PUT to create (or update) an external adjunct directly at its path. The id
    is taken from the URL path element, so it is optional in the body."""
    path = (
        f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}"
        f"/images/{asset_id}/adjuncts/{adjunct_id}"
    )
    adjunct = {
        "externalId": external_adjunct_url,
        "@type": "Dataset",
        "mediaType": "text/xml",
        "profile": "http://www.loc.gov/standards/alto/v3/alto.xsd",
        "label": {"en": ["METS-ALTO XML (external, via PUT)"]},
        "size": 36032,
        "iiifLink": "seeAlso",
        "language": ["en"]
    }
    r = put_resource(path, adjunct)
    print("PUT external adjunct returned:")
    pprint(r.json())
    print()


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

    # Create an external adjunct via POST
    post_external_adjunct()

    # GET to verify - publicId will equal the externalId
    get_adjunct()

    # Clean up
    delete_adjunct()

    # Alternative: create via PUT directly to the adjunct's path
    put_external_adjunct()

    # GET to verify
    get_adjunct()

    # Clean up
    delete_adjunct()
