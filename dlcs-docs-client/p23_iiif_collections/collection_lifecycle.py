import requests
import settings
from iiif_cs import (PRESENTATION_HEADERS, get_iiif_resource, post_iiif_resource,
                     put_iiif_resource, delete_iiif_resource, pprint)

customer = settings.IIIF_CS_CUSTOMER_ID
host = settings.IIIF_CS_PRESENTATION_HOST
root = f"{host}/{customer}/collections/root"


def storage_collection(label, slug, parent):
    return {
        "type": "Collection",
        "behavior": ["storage-collection", "public-iiif"],
        "label": {"en": [label]},
        "slug": slug,
        "parent": parent,
    }


# 1. POST a new storage collection to the flat container URL - the platform
#    mints the flat identifier and returns it in the Location header
r = post_iiif_resource(f"/{customer}/collections",
                       storage_collection("Docs example collection", "docs-collection-example", root))
parent_url = r.headers["Location"]
print(f"Created (minted): {parent_url}")
print()

# 2. PUT a child storage collection at a flat identifier we choose ourselves
child_url = f"{host}/{customer}/collections/docs-example-child"
r = put_iiif_resource(f"/{customer}/collections/docs-example-child",
                      storage_collection("A child collection", "child-a", parent_url))
print(f"Created (chosen id): {r.json()['id']}")
print()

# 3. POST a IIIF Collection child - no storage-collection behavior, and we
#    supply the items ourselves; they can reference any IIIF anywhere
r = post_iiif_resource(f"/{customer}/collections", {
    "type": "Collection",
    "behavior": ["public-iiif"],
    "label": {"en": ["A IIIF Collection"]},
    "slug": "child-b",
    "parent": parent_url,
    "items": [
        {
            "id": "https://example.org/iiif/some-external-manifest.json",
            "type": "Manifest",
            "label": {"en": ["An external manifest"]}
        }
    ]
})
iiif_col_url = r.headers["Location"]
print(f"Created IIIF Collection: {iiif_col_url}")
print()

# 4. The parent's API view now shows totals and generated items
r = get_iiif_resource(parent_url)
parent = r.json()
print("Parent totals:", parent["totals"])
for item in parent["items"]:
    print("  child:", item["label"]["en"][0], item.get("behavior", "(a Manifest would have no behavior)"))
print()

# 5. Order by slug, two to a page - the view links carry the ordering through
r = requests.get(f"{parent_url}?orderBy=slug&pageSize=1", headers=PRESENTATION_HEADERS)
page = r.json()
print("Page 1 ordered by slug:", [i["label"]["en"][0] for i in page["items"]])
print("Next page link:", page["view"]["next"])
print()

# 6. Rename the parent (PUT with a new slug) - the child's PUBLIC URL changes
#    too, because public URLs are built from the chain of slugs; flat URLs
#    never change
child_public_before = get_iiif_resource(child_url).json()["publicId"]
r = get_iiif_resource(parent_url)
body = storage_collection("Docs example collection", "docs-collection-renamed", root)
put_iiif_resource(parent_url, body, etag=r.headers["ETag"])
child_public_after = get_iiif_resource(child_url).json()["publicId"]
print("Child public URL before rename:", child_public_before)
print("Child public URL after rename: ", child_public_after)
print()

# 7. Clean up. Children first: a collection with children cannot be deleted
r = get_iiif_resource(parent_url)
r = delete_iiif_resource(parent_url, r.headers["ETag"])
print(f"DELETE parent while it still has children: {r.status_code}")
pprint(r.json())

for url in [child_url, iiif_col_url, parent_url]:
    r = get_iiif_resource(url)
    d = delete_iiif_resource(url, r.headers["ETag"])
    print(f"DELETE {url.rsplit('/', 1)[-1]}: {d.status_code}")
