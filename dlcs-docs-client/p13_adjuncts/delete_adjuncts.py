import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, post_resource, pprint
from p07_asset.asset_adjuncts import ensure_rusty_boat_asset, rusty_boat_asset_id

# Two external adjuncts to create and then delete in one request
external_url = (
    "https://dlcsstage-public-test-objects.s3.eu-west-1.amazonaws.com"
    "/images-with-text/b29820947_0014.jp2.xml"
)
adjunct_ids = ["bulk-delete-1.xml", "bulk-delete-2.xml"]


def post_two_adjuncts(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """POST two external adjuncts to the asset so there is something to bulk-delete."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}/adjuncts"
    members = [
        {
            "id": adjunct_id,
            "externalId": external_url,
            "@type": "Dataset",
            "mediaType": "text/xml",
            "label": {"en": [f"Throwaway adjunct {adjunct_id}"]},
            "iiifLink": "seeAlso"
        }
        for adjunct_id in adjunct_ids
    ]
    r = post_resource(path, members)
    print(f"POST two adjuncts returned status: {r.status_code}")
    print()


def delete_adjuncts(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """POST a collection to /customers/{customer}/deleteAdjuncts. Each member names an
    asset by its full id (customer/space/asset) and lists the adjunct ids to delete."""
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/deleteAdjuncts"
    body = {
        "@context": "http://www.w3.org/ns/hydra/context.jsonld",
        "@type": "Collection",
        "member": [
            {
                "id": f"{settings.IIIF_CS_CUSTOMER_ID}/{space_id}/{asset_id}",
                "adjunct": adjunct_ids
            }
        ]
    }
    r = post_resource(path, body)
    print(f"POST deleteAdjuncts returned status: {r.status_code}")
    print()


def get_adjunct_status(adjunct_id, asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """GET an adjunct and report the status - 404 once deleted."""
    path = (
        f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}"
        f"/images/{asset_id}/adjuncts/{adjunct_id}"
    )
    r = get_cloud_services_resource(path)
    print(f"GET {adjunct_id} returned status: {r.status_code}")
    print()


if __name__ == '__main__':
    ensure_rusty_boat_asset()

    post_two_adjuncts()
    for adjunct_id in adjunct_ids:
        get_adjunct_status(adjunct_id)   # 200

    delete_adjuncts()                    # 204

    for adjunct_id in adjunct_ids:
        get_adjunct_status(adjunct_id)   # 404
