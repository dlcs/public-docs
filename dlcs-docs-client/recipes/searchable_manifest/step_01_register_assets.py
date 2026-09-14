"""Step 1: register the page images as assets, in reading order."""
import time
from iiif_cs import post_resource, get_cloud_services_resource
from recipes.searchable_manifest.recipe_settings import (
    customer, space, PAGES, FIXTURE_BASE, asset_id_prefix)

# One batch of eight images. number1 carries the page sequence and string1
# groups the set - the standard metadata pattern for an ordered sequence.
members = [
    {
        "id": f"{asset_id_prefix}_{page}",
        "space": space,
        "origin": f"{FIXTURE_BASE}/{page}.jpg",
        "mediaType": "image/jpeg",
        "string1": "energy-index",
        "number1": int(page),
    }
    for page in PAGES
]

r = post_resource(f"/customers/{customer}/queue", {"member": members})
batch = r.json()
print(f"Batch created: {batch['@id']}")

# Wait for the whole batch to finish
batch_path = batch["@id"].split(f"/customers/{customer}", 1)[1]
while True:
    b = get_cloud_services_resource(f"/customers/{customer}{batch_path}").json()
    print(f"completed {b['completed']} of {b['count']}, errors: {b['errors']}")
    if b["completed"] + b["errors"] >= b["count"]:
        break
    time.sleep(5)
