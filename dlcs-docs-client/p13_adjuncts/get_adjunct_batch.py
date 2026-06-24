import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, post_resource, delete_resource, wait_for_value, pprint
from p07_asset.asset_adjuncts import ensure_rusty_boat_asset, rusty_boat_asset_id

adjunct_id = "batch-demo.txt"


def post_adjunct_via_queue(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """POST adjuncts to the adjunct queue. The platform creates an AdjunctBatch
    and processes the adjuncts asynchronously. Each adjunct gains a 'batch' link
    pointing to the batch it was most recently ingested in."""
    collection = {
        "member": [
            {
                "id": adjunct_id,
                "space": space_id,
                "image": asset_id,
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/adjuncts/rusty-boat.txt",
                "@type": "Text",
                "mediaType": "text/plain",
                "label": {"en": ["Description of the rusty boat image"]},
                "iiifLink": "seeAlso",
                "language": ["en"]
            }
        ]
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/adjunctQueue"
    r = post_resource(path, collection)
    print("POST to adjunct queue returned:")
    batch = r.json()
    pprint(batch)
    print()
    return batch


def get_adjunct_batch_link(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """GET the adjunct and follow its 'batch' link to retrieve the AdjunctBatch.
    Only adjuncts submitted via the adjunct queue will have a batch link."""
    adjunct_path = (
        f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}"
        f"/images/{asset_id}/adjuncts/{adjunct_id}"
    )
    adjunct = get_cloud_services_resource(adjunct_path).json()
    print("GET adjunct returned:")
    pprint(adjunct)
    print()

    batch_link = adjunct.get("batch")
    if not batch_link:
        print("Adjunct has no batch link — it was not submitted via the queue.")
        return None

    print(f"Following batch link: {batch_link}")
    print()
    batch = get_cloud_services_resource(batch_link).json()
    print("GET AdjunctBatch returned:")
    pprint(batch)
    print()
    return batch


def delete_adjunct(asset_id=rusty_boat_asset_id, space_id=docs_space_id):
    """DELETE the adjunct created by this script."""
    path = (
        f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}"
        f"/images/{asset_id}/adjuncts/{adjunct_id}"
    )
    r = delete_resource(path)
    print(f"DELETE adjunct returned status: {r.status_code}")
    print()


if __name__ == '__main__':
    ensure_rusty_boat_asset()

    # Submit adjunct via the queue - it gains a batch link on ingestion
    post_adjunct_via_queue()

    # Wait until the adjunct has been ingested
    adjunct_path = (
        f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{docs_space_id}"
        f"/images/{rusty_boat_asset_id}/adjuncts/{adjunct_id}"
    )
    wait_for_value(path=adjunct_path, field="ingesting", value=False, interval=2, retries=10)

    # GET adjunct and follow its batch link
    get_adjunct_batch_link()

    # Clean up
    delete_adjunct()
