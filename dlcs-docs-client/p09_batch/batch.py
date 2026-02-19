import settings
from iiif_cs import get_cloud_services_resource, post_resource, pprint
from p08_queue.get_batches import get_batches


def get_batch(batch_url):
    """GET a specific batch by its URL."""
    r = get_cloud_services_resource(batch_url)
    print("GET Batch returned:")
    batch = r.json()
    pprint(batch)
    print()
    return batch


def get_batch_images(batch):
    """GET the collection of assets currently associated with this batch.
    An asset belongs to only one batch: the most recent batch it was part of.
    If assets have been re-submitted in a later batch, they will not appear here.
    """
    images_url = batch["images"]
    r = get_cloud_services_resource(images_url)
    print("GET Batch images returned:")
    images = r.json()
    pprint(images)
    print()
    return images


def get_batch_assets(batch):
    """GET the collection of all assets originally submitted in this batch.
    Unlike images, this includes assets that have since been claimed by a later batch.
    """
    # TODO: use batch["assets"] once the property is returned by the API
    assets_url = batch["@id"] + "/assets"
    r = get_cloud_services_resource(assets_url)
    print("GET Batch assets returned:")
    assets = r.json()
    pprint(assets)
    print()
    return assets


def test_batch(batch):
    """POST to the batch test endpoint to force an update of the superseded property."""
    test_url = batch["test"]
    r = post_resource(test_url, {})
    print("POST to batch test returned:")
    result = r.json()
    pprint(result)
    print()
    return result


if __name__ == '__main__':
    # Get the list of batches and use the most recent one
    batches = get_batches()
    members = batches.get("member", [])
    if not members:
        print("No batches found. Submit assets to the queue first.")
    else:
        batch_url = members[0]["@id"]
        batch = get_batch(batch_url)

        get_batch_images(batch)
        get_batch_assets(batch)
        test_batch(batch)
