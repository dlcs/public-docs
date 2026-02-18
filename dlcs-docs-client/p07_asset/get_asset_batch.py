import settings
from settings import docs_space_id
from iiif_cs import get_cloud_services_resource, pprint

# Asset ID created via the queue in p02_registering/post_to_queue.py
queue_asset_id = "post-to-queue-example-1-rhine"


def get_asset_batch(asset_id=queue_asset_id, space_id=docs_space_id):
    """
    Get the batch that an asset was ingested in.
    Only assets registered via the queue will have a batch link.
    Assets created directly via PUT will not have a batch.
    """
    # First, get the asset
    asset_path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/spaces/{space_id}/images/{asset_id}"
    asset_response = get_cloud_services_resource(asset_path)

    # If asset doesn't exist, create it via the queue
    if asset_response.status_code == 404:
        print(f"Asset {asset_id} does not exist. Creating via queue...")
        print()
        from p02_registering.post_to_queue import post_asset_to_queue
        post_asset_to_queue()
        # Re-fetch the asset
        asset_response = get_cloud_services_resource(asset_path)

    asset = asset_response.json()

    # Check if the asset has a batch link
    batch_link = asset.get("batch")
    if not batch_link:
        print(f"Asset {asset_id} does not have a batch link.")
        print("This asset was likely created directly via PUT, not via the queue.")
        return None

    print(f"Asset has batch link: {batch_link}")
    print()

    # Follow the batch link
    batch_response = get_cloud_services_resource(batch_link)
    batch = batch_response.json()
    print("GET Batch returned:")
    pprint(batch)
    print()
    return batch


if __name__ == '__main__':
    get_asset_batch()
