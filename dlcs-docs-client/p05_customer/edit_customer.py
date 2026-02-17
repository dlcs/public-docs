from time import strftime

import settings
from iiif_cs import patch_resource, pprint


def edit_customer():
    patch = {
      "displayName": f"Display name edited on {strftime("%d/%m/%y at %I:%M%p")}"
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}"
    r = patch_resource(path, patch)
    print("PATCH returned:")
    pprint(r.json())
    print()


if __name__ == '__main__':
    edit_customer()