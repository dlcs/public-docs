import requests
import settings
from iiif_cs import (PRESENTATION_HEADERS, get_iiif_resource, post_iiif_resource,
                     delete_iiif_resource, pprint)

customer = settings.IIIF_CS_CUSTOMER_ID
host = settings.IIIF_CS_PRESENTATION_HOST
root = f"{host}/{customer}/collections/root"
search_url = f"{root}/search"

# 1. Create two storage collections with distinctive labels to find
created = []
for label, slug in [("Alpha printing works", "docs-search-alpha"),
                    ("Beta printing works", "docs-search-beta")]:
    r = post_iiif_resource(f"/{customer}/collections", {
        "type": "Collection",
        "behavior": ["storage-collection", "public-iiif"],
        "label": {"en": [label]},
        "slug": slug,
        "parent": root,
    })
    created.append(r.headers["Location"])
    print(f"Created: {label}")
print()

# 2. Search for them by label. Search needs credentials AND the Show-Extras
#    header, and matches across ALL your resources - collections and manifests
r = requests.get(f"{search_url}?label=printing", headers=PRESENTATION_HEADERS)
results = r.json()
print(f"Search for 'printing': HTTP {r.status_code}, {results['totalItems']} matches")
print("Result label:", results["label"]["en"][0])
for item in results["items"]:
    print("  match:", item["type"], "-", item["label"]["en"][0])
print()

# 3. Search terms must be at least 3 characters
r = requests.get(f"{search_url}?label=ab", headers=PRESENTATION_HEADERS)
print(f"Search for 'ab': HTTP {r.status_code}")
pprint(r.json())
print()

# 4. Clean up
for url in created:
    r = get_iiif_resource(url)
    d = delete_iiif_resource(url, r.headers["ETag"])
    print(f"DELETE {url.rsplit('/', 1)[-1]}: {d.status_code}")
