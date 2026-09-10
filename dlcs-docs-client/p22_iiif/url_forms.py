import requests
import settings
from iiif_cs import BASIC_AUTH_HEADER, get_iiif_resource

# Every customer has a root storage collection, available at two URLs:
#   hierarchical (canonical for the public): {host}/{customer}
#   flat (fixed identity, hosts the API view): {host}/{customer}/collections/root
customer = settings.IIIF_CS_CUSTOMER_ID
hierarchical = f"{settings.IIIF_CS_PRESENTATION_HOST}/{customer}"
flat = f"{settings.IIIF_CS_PRESENTATION_HOST}/{customer}/collections/root"


def show(label, response):
    line = f"{label}: HTTP {response.status_code}"
    location = response.headers.get("Location")
    if location:
        line += f" -> {location}"
    print(line)


# 1. A public (anonymous) client GETs the hierarchical URL: plain IIIF
r = requests.get(hierarchical)
show("1. public GET, hierarchical", r)
print("   @context:", r.json()["@context"])
print()

# 2. The flat URL redirects a public client to the canonical hierarchical form
r = requests.get(flat, allow_redirects=False)
show("2. public GET, flat", r)
print()

# 3. Credentials alone make no difference to a GET - still the public view
r = requests.get(flat, headers={**BASIC_AUTH_HEADER}, allow_redirects=False)
show("3. authorized GET, flat, no Show-Extras", r)
print()

# 4. Credentials + X-IIIF-CS-Show-Extras: the API view lives at the FLAT URL,
#    so now the hierarchical URL redirects the other way
r = requests.get(hierarchical,
                 headers={**BASIC_AUTH_HEADER, "X-IIIF-CS-Show-Extras": "All"},
                 allow_redirects=False)
show("4. API-view GET, hierarchical", r)
print()

# 5. ... and the flat URL returns the API view: still valid IIIF, with an extra
#    @context and extra properties for managing the resource
r = get_iiif_resource(f"/{customer}/collections/root")
collection = r.json()
print("   @context:", collection["@context"])
extras = [k for k in ("publicId", "flatId", "slug", "parent", "behavior", "created", "modified", "totals")
          if k in collection]
print("   extra properties present:", extras)
print()

# 6. Show-Extras without credentials is ignored - back to the public behaviour
r = requests.get(flat, headers={"X-IIIF-CS-Show-Extras": "All"}, allow_redirects=False)
show("6. Show-Extras but NO credentials", r)
