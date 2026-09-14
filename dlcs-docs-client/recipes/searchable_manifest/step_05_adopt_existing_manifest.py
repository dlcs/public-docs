"""Variant: starting from an EXISTING manifest that uses platform assets.

If you already have your own manifest - authored elsewhere, painting image
services this platform provides - you can "adopt" it: save it to the platform,
then convert it to paintedResources in one update. Your canvas ids are
preserved, the assets are NOT reingested, and the text pipeline then runs.

This script first builds a stand-in for "your existing manifest" (an ordinary
IIIF document over two of the recipe's assets), then performs the adoption.
"""
import json
import time
import requests
from iiif_cs import (get_iiif_resource, put_iiif_resource, delete_iiif_resource,
                     get_cloud_services_resource)
from recipes.searchable_manifest.recipe_settings import (
    customer, space, asset_id_prefix, presentation_host)

public_host = presentation_host.replace("//presentation-api.", "//", 1)
root = f"{presentation_host}/{customer}/collections/root"
adopt_path = f"/{customer}/manifests/energy-index-adopted"


def canvas_for(page, order):
    """A canvas exactly as an external manifest would author it: its own id,
    painting the platform's image service for the asset."""
    asset = f"{asset_id_prefix}_{page}"
    canvas_id = f"{presentation_host}/{customer}/canvases/energy-adopted-{page}"
    service = f"{public_host}/iiif-img/{customer}/{space}/{asset}"
    return {
        "id": canvas_id, "type": "Canvas", "width": 1338, "height": 2240,
        "items": [{
            "id": f"{canvas_id}/page", "type": "AnnotationPage",
            "items": [{
                "id": f"{canvas_id}/page/1", "type": "Annotation", "motivation": "painting",
                "body": {"id": f"{service}/full/598,1024/0/default.jpg", "type": "Image",
                         "format": "image/jpeg", "width": 598, "height": 1024,
                         "service": [{"@context": "http://iiif.io/api/image/3/context.json",
                                      "id": service, "type": "ImageService3", "profile": "level2"}]},
                "target": canvas_id}]}]}


# 0. Clean up any previous run, then save "your existing manifest" as-is
r = get_iiif_resource(adopt_path)
if r.status_code == 200:
    delete_iiif_resource(adopt_path, r.headers["ETag"])

existing = {"type": "Manifest", "label": {"en": ["My existing manifest"]},
            "slug": "energy-index-adopted", "parent": root,
            "items": [canvas_for("0003", 0), canvas_for("0004", 1)]}
r = put_iiif_resource(adopt_path, existing)
print(f"Saved the existing manifest as-is: {r.status_code}")
g = get_iiif_resource(adopt_path)
authored_ids = [c["id"] for c in g.json()["items"]]
batch_before = get_cloud_services_resource(
    f"/customers/{customer}/spaces/{space}/images/{asset_id_prefix}_0003").json()["batch"]

# 1. ADOPT: one update - canvases become empty placeholders KEEPING their ids,
#    paintedResources attach the assets to those same canvas ids (adding the
#    OCR adjuncts inline), and the text pipeline is requested.
adoption = {
    "type": "Manifest", "label": {"en": ["My existing manifest"]},
    "slug": "energy-index-adopted", "parent": root,
    "items": [{"id": cid, "type": "Canvas"} for cid in authored_ids],
    # The assets already carry their OCR adjuncts (from step 3), so the
    # adoption references the assets plainly - no need to restate adjuncts.
    "paintedResources": [
        {"asset": {"id": f"{asset_id_prefix}_{page}", "space": space},
         "canvasPainting": {"canvasId": cid, "canvasOrder": order}}
        for order, (page, cid) in enumerate(zip(["0003", "0004"], authored_ids))
    ],
    "pipeline": [{"name": "text", "config": {"action": "Index"}}],
}
r = put_iiif_resource(adopt_path, adoption, etag=g.headers["ETag"])
print(f"Adoption update: {r.status_code}")

while True:
    body = get_iiif_resource(adopt_path).json()
    if not body.get("ingesting") and not body.get("pipeline"):
        break
    time.sleep(6)
# "Completed" means the text was indexed. "CompletedNoOperation" means the
# pipeline found no words - a known platform issue on this adoption path,
# see https://github.com/dlcs/iiif-presentation/issues/677
print("Pipeline:", body["finishedPipelines"][0]["status"])

# 2. Prove the important properties of adoption
batch_after = get_cloud_services_resource(
    f"/customers/{customer}/spaces/{space}/images/{asset_id_prefix}_0003").json()["batch"]
print("Assets were NOT reingested:", batch_before == batch_after)
public = requests.get(body["publicId"], allow_redirects=True).json()
print("Canvas ids preserved:", [c["id"] for c in public["items"]] == authored_ids)
print("OCR on canvases:", all(bool(c.get("seeAlso")) for c in public["items"]))
print("Search service:", bool(public.get("service")))

# 3. This was a demonstration - clean it up
g = get_iiif_resource(adopt_path)
d = delete_iiif_resource(adopt_path, g.headers["ETag"])
print(f"Cleaned up the demonstration manifest: {d.status_code}")
