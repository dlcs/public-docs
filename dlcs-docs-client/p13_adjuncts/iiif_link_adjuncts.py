import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, post_resource, delete_resource, pprint
from p07_asset.asset_adjuncts import ensure_rusty_boat_asset, rusty_boat_asset_id

# S3 test objects used as origins - same as in the documentation example
s3_base = "https://dlcsstage-public-test-objects.s3.eu-west-1.amazonaws.com/images-with-text"

adjunct_ids = [
    "mets-from-origin.xml",
    "annotations-from-origin.json",
    "rendering-from-origin.jpg",
    "text-from-origin.txt",
    "link-unspecified-from-external.xml",
]


def post_iiif_link_adjuncts(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """POST five adjuncts in one request, each with a different iiifLink value.
    The iiifLink property controls how each adjunct appears in generated IIIF:
      - seeAlso:          listed under the Canvas seeAlso property
      - annotations:      listed directly under the Canvas annotations property
      - rendering:        listed under the Canvas rendering property
      - inlineAnnotation: expressed as a body within a platform-managed AnnotationPage
      - (none):           listed under the non-standard otherAdjuncts property
    """
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}/adjuncts"
    adjuncts = [
        {
            "id": "mets-from-origin.xml",
            "origin": f"{s3_base}/b29820947_0014.jp2.xml",
            "@type": "Dataset",
            "mediaType": "text/xml",
            "profile": "http://www.loc.gov/standards/alto/v3/alto.xsd",
            "label": {"en": ["METS-ALTO XML"]},
            "iiifLink": "seeAlso",
            "language": ["en-GB", "cy"]
        },
        {
            "id": "annotations-from-origin.json",
            "origin": f"{s3_base}/b29820947_0014.jp2.line.json",
            "@type": "AnnotationPage",
            "label": {"en": ["Line-level annotations"]},
            "iiifLink": "annotations",
            "language": ["en", "cy"]
        },
        {
            "id": "rendering-from-origin.jpg",
            "origin": f"{s3_base}/b29820947_0014.jp2.jpg",
            "@type": "Image",
            "mediaType": "image/jpeg",
            "label": {"en": ["A JPEG of the asset"]},
            "iiifLink": "rendering"
        },
        {
            "id": "text-from-origin.txt",
            "origin": f"{s3_base}/b29820947_0014.jp2.txt",
            "@type": "Text",
            "mediaType": "text/plain",
            "label": {"en": ["Plain text of this page"]},
            "language": ["en", "cy"],
            "iiifLink": "inlineAnnotation",
            "motivation": "supplementing",
            "provides": "transcript"
        },
        {
            # No iiifLink - will appear under otherAdjuncts in generated IIIF
            "id": "link-unspecified-from-external.xml",
            "externalId": f"{s3_base}/b29820947_0014.jp2.xml",
            "@type": "Text",
            "mediaType": "text/xml",
            "label": {"en": ["A link to a resource without a IIIF expression"]}
        }
    ]
    r = post_resource(path, adjuncts)
    print("POST five adjuncts returned:")
    pprint(r.json())
    print()


def get_adjuncts(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """GET the adjuncts collection to confirm all five adjuncts were created."""
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

    # POST all five adjuncts in one request, each with a different iiifLink value
    post_iiif_link_adjuncts()

    # GET the collection to confirm all five are present
    get_adjuncts()

    # Clean up
    for adjunct_id in adjunct_ids:
        delete_adjunct(adjunct_id)
