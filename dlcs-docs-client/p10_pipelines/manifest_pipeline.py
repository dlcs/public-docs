import time
import requests
import settings
from iiif_cs import (get_iiif_resource, put_iiif_resource, delete_iiif_resource,
                     post_resource, delete_resource, pprint)

customer = settings.IIIF_CS_CUSTOMER_ID
host = settings.IIIF_CS_PRESENTATION_HOST
root = f"{host}/{customer}/collections/root"
space = settings.docs_space_id

# The text pipeline indexes the text adjuncts of the manifest's assets.
# Give page_01 an ALTO adjunct and a plain-text adjunct to be indexed.
s3_base = "https://dlcsstage-public-test-objects.s3.eu-west-1.amazonaws.com/images-with-text"
adjuncts_path = f"/customers/{customer}/spaces/{space}/images/page_01/adjuncts"
r = post_resource(adjuncts_path, [
    {
        "id": "docs-alto.xml",
        "origin": f"{s3_base}/b29820947_0014.jp2.xml",
        "@type": "Dataset",
        "mediaType": "text/xml",
        "profile": "http://www.loc.gov/standards/alto/v3/alto.xsd",
        "label": {"en": ["ALTO XML"]},
        "iiifLink": "seeAlso"
    },
    {
        "id": "docs-text.txt",
        "origin": "https://dlcs.github.io/public-docs/doc_fixtures/adjuncts/rusty-boat.txt",
        "@type": "Text",
        "mediaType": "text/plain",
        "label": {"en": ["Plain text of this page"]},
        "iiifLink": "inlineAnnotation",
        "motivation": "supplementing",
        "provides": "transcript"
    }
])
print(f"Added text adjuncts to page_01: {r.status_code}")
print()

# Create a manifest painting that asset, with the text pipeline requested
manifest = {
    "type": "Manifest",
    "label": {"en": ["A manifest with searchable text"]},
    "slug": "docs-manifest-pipeline",
    "parent": root,
    "paintedResources": [
        {"asset": {"id": "page_01", "space": space}, "canvasPainting": {"canvasOrder": 0}}
    ],
    "pipeline": [
        {"name": "text", "config": {"action": "Index"}}
    ]
}
r = put_iiif_resource(f"/{customer}/manifests/docs-manifest-pipeline", manifest)
print(f"Create returned {r.status_code}")
public_id = r.json()["publicId"]

# While the pipeline runs, the manifest is staged - not yet public
print("Public GET while pipeline pending:", requests.get(public_id).status_code)
print()

# Poll until the job moves from pipeline to finishedPipelines
while True:
    r = get_iiif_resource(f"/{customer}/manifests/docs-manifest-pipeline")
    body = r.json()
    if not body.get("pipeline"):
        break
    print("pipeline:", body["pipeline"][0]["status"])
    time.sleep(5)
print("finishedPipelines:")
pprint(body["finishedPipelines"])
print()

# The public manifest now exists, carrying a IIIF Content Search 2 service
public = requests.get(public_id, allow_redirects=True).json()
print("Public manifest service:")
pprint(public["service"])
print()

# Clean up: the manifest (which also removes its text-search artefacts),
# then the adjuncts we added
r = get_iiif_resource(f"/{customer}/manifests/docs-manifest-pipeline")
d = delete_iiif_resource(f"/{customer}/manifests/docs-manifest-pipeline", r.headers["ETag"])
print(f"DELETE manifest: {d.status_code}")
for adjunct_id in ("docs-alto.xml", "docs-text.txt"):
    d = delete_resource(f"{adjuncts_path}/{adjunct_id}")
    print(f"DELETE adjunct {adjunct_id}: {d.status_code}")
