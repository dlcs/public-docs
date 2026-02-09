import settings
from iiif_cs import patch_resource, pprint


def edit_customer():
    patch = {
      "displayName": "An edited customer"
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}"
    r = patch_resource(path, patch)
    print("PATCH returned:")
    pprint(r.json())
    print()


if __name__ == '__main__':
    edit_customer()