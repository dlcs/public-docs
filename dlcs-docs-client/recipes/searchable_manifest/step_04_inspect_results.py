"""Step 4: inspect what you now have - the enriched public manifest, and search."""
import requests
from iiif_cs import get_iiif_resource, pprint
from recipes.searchable_manifest.recipe_settings import manifest_path

api_view = get_iiif_resource(manifest_path).json()
public = requests.get(api_view["publicId"], allow_redirects=True).json()

print(f"Public manifest: {public['id']}")
print(f"Canvases: {len(public['items'])}")
first = public["items"][0]
print("First canvas seeAlso (the OCR text, hosted by the platform):")
pprint(first.get("seeAlso"))
print()
print("Manifest-level service (IIIF Content Search 2, with autocomplete):")
pprint(public.get("service"))
print()

# Use the search service like a viewer would
search_id = public["service"][0]["id"]
for term in ("energy", "pressure"):
    hits = requests.get(f"{search_id}?q={term}").json().get("items", [])
    print(f"Search '{term}': {len(hits)} hits")
    for hit in hits[:2]:
        print("   ", hit.get("target", ""))
