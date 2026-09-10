import time
import requests
import settings
from iiif_cs import (get_iiif_resource, put_iiif_resource, delete_iiif_resource,
                     get_cloud_services_resource, delete_resource)

customer = settings.IIIF_CS_CUSTOMER_ID
host = settings.IIIF_CS_PRESENTATION_HOST
root = f"{host}/{customer}/collections/root"
space = settings.docs_space_id

# Build a manifest from two existing assets plus one NEW asset, registered
# through the manifest itself. The new asset's object is a normal asset
# registration - origin, mediaType and so on - and because it has no "space",
# it will land in a Space created on demand for this manifest.
manifest = {
    "type": "Manifest",
    "label": {"en": ["A manifest from assets"]},
    "slug": "docs-manifest-from-assets",
    "parent": root,
    "paintedResources": [
        {
            "asset": {"id": "page_01", "space": space},
            "canvasPainting": {"canvasOrder": 0, "label": {"en": ["Page 1 (existing asset)"]}}
        },
        {
            "asset": {"id": "page_02", "space": space},
            "canvasPainting": {"canvasOrder": 1, "label": {"en": ["Page 2 (existing asset)"]}}
        },
        {
            "asset": {
                "id": "page_04",
                "mediaType": "image/jpeg",
                "origin": "https://dlcs.github.io/public-docs/doc_fixtures/printed-seq/04.jpg"
            },
            "canvasPainting": {"canvasOrder": 2, "label": {"en": ["Page 4 (a NEW asset)"]}}
        }
    ]
}

r = put_iiif_resource(f"/{customer}/manifests/docs-manifest-from-assets", manifest)
print(f"Create returned {r.status_code} (202 = accepted, ingest in progress)")
manifest_space = r.json()["space"]
print("The manifest's on-demand space:", manifest_space)
print("ingesting:", r.json().get("ingesting"))
print()

# Poll the manifest until the ingesting property disappears
while True:
    r = get_iiif_resource(f"/{customer}/manifests/docs-manifest-from-assets")
    ingesting = r.json().get("ingesting")
    print("poll - ingesting:", ingesting)
    if not ingesting:
        break
    time.sleep(5)
print()

# The public manifest now has three canvases, each painting an image service.
# Note the new asset's image service lives in the manifest's own space.
public = requests.get(r.json()["publicId"]).json()
print(f"Public manifest has {len(public['items'])} canvases:")
for canvas in public["items"]:
    body = canvas["items"][0]["items"][0]["body"]
    print("  ", canvas["label"]["en"][0], "->", body["id"])
print()

# Clean up. Deleting a manifest does NOT delete its assets or its space -
# they are ordinary platform resources, managed via the main API.
r = get_iiif_resource(f"/{customer}/manifests/docs-manifest-from-assets")
d = delete_iiif_resource(f"/{customer}/manifests/docs-manifest-from-assets", r.headers["ETag"])
print(f"DELETE manifest: {d.status_code}")

space_path = manifest_space.replace(settings.IIIF_CS_API_HOST, "")
for image in get_cloud_services_resource(f"{space_path}/images").json()["member"]:
    d = delete_resource(image["@id"].replace(settings.IIIF_CS_API_HOST, ""))
    print(f"DELETE asset {image['id']}: {d.status_code}")
d = delete_resource(space_path)
print(f"DELETE the manifest's space: {d.status_code}")
