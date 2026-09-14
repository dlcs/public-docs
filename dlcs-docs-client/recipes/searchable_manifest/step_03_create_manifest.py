"""Step 3: create the Manifest - one call does everything.

The single PUT below:
  - creates the Manifest, generating a canvas per asset in canvasOrder;
  - registers an ALTO adjunct against each asset (fetched from its origin);
  - expresses each adjunct as a seeAlso link on its canvas;
  - queues the text pipeline, which indexes the ALTO for search.
"""
import json
import time
from iiif_cs import get_iiif_resource, put_iiif_resource, delete_iiif_resource
from recipes.searchable_manifest.recipe_settings import (
    customer, space, PAGES, FIXTURE_BASE, asset_id_prefix,
    manifest_slug, manifest_path, presentation_host)

manifest = {
    "type": "Manifest",
    "label": {"en": ["The energy index"]},
    "metadata": [
        {"label": {"en": ["Author"]}, "value": {"en": ["Joseph H. Barach"]}},
        {"label": {"en": ["Source"]},
         "value": {"en": ["Wellcome Collection b3343136x (Public Domain Mark 1.0)"]}},
    ],
    "slug": manifest_slug,
    "parent": f"{presentation_host}/{customer}/collections/root",
    "paintedResources": [
        {
            "asset": {
                "id": f"{asset_id_prefix}_{page}",
                "space": space,
                "adjuncts": [
                    {
                        "id": "alto.xml",
                        "origin": f"{FIXTURE_BASE}/alto/{page}.xml",
                        "@type": "Dataset",
                        "mediaType": "text/xml",
                        "profile": "http://www.loc.gov/standards/alto/v3/alto.xsd",
                        "label": {"en": [f"OCR text for page {int(page)}"]},
                        "iiifLink": "seeAlso"
                    }
                ]
            },
            "canvasPainting": {
                "canvasOrder": int(page) - 1,
                "label": {"en": [f"Page {int(page)}"]}
            }
        }
        for page in PAGES
    ],
    "pipeline": [
        {"name": "text", "config": {"action": "Index"}}
    ]
}

# Make the script re-runnable: remove any previous version of this manifest
r = get_iiif_resource(manifest_path)
if r.status_code == 200:
    delete_iiif_resource(manifest_path, r.headers["ETag"])
    print("(removed the previous version)")

r = put_iiif_resource(manifest_path, manifest)
print(f"Create returned {r.status_code} (202 = accepted, work in progress)")

# Wait for asset/adjunct ingest and the pipeline to finish
while True:
    body = get_iiif_resource(manifest_path).json()
    ingesting, pipeline = body.get("ingesting"), body.get("pipeline")
    print("ingesting:", json.dumps(ingesting), "| pipeline:",
          pipeline[0]["status"] if pipeline else None)
    if not ingesting and not pipeline:
        break
    time.sleep(6)

print()
print("finishedPipelines:")
print(json.dumps(body["finishedPipelines"], indent=2))
print()
print("Public manifest:", body["publicId"])
