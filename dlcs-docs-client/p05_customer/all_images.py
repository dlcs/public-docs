import settings
from iiif_cs import post_resource, pprint, get_cloud_services_resource, patch_resource


def post_all_images_2025():
    space = 1
    collection = {
      "member": [
        # replace these with your own existing examples
        { "id": f"{settings.IIIF_CS_CUSTOMER_ID}/{space}/put-example-1-rusty-boat" },
        { "id": f"{settings.IIIF_CS_CUSTOMER_ID}/{space}/page_03" }
      ]
    }
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/allImages"
    r = post_resource(path, collection)
    print("POST returned:")
    images = r.json()
    pprint(images)
    print(f"{len(images['member'])} assets returned.")
    print()


def get_all_images():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/allImages"
    r = get_cloud_services_resource(path)
    print("GET returned:")
    images = r.json()
    pprint(images)
    print(f"{len(images['member'])} assets returned.")
    print()


def get_all_images_with_query():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/allImages"
    # replace with your own example values
    query = '?q={"string1":"catalogue-1985"}' # or ?string1=catalogue-1985
    r = get_cloud_services_resource(path + query)
    print("GET returned:")
    images = r.json()
    pprint(images)
    print(f"{len(images['member'])} assets returned.")
    print()


# TODO: Unsupported
def patch_all_images_with_query():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/allImages"
    query = '?string1=catalogue-1985'
    patch = {
        "@type": "Collection",
        "field": "string2",
        "operation": "replace",
        "value": ["patched-2"]
    }
    r = patch_resource(path + query, patch)
    print("PATCH returned:")
    images = r.json()
    pprint(images)
    print(f"{len(images['member'])} assets returned.")
    print()


# TODO: Unsupported
def patch_all_images_with_members():
    space = 1
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/allImages"
    patch = {
        "@type": "Collection",
        "member": [
            # replace these with your own existing examples
            { "id": f"{settings.IIIF_CS_CUSTOMER_ID}/{space}/put-example-1-rusty-boat" },
            { "id": f"{settings.IIIF_CS_CUSTOMER_ID}/{space}/page_03" }
        ],
        "field": "string2",
        "operation": "replace",
        "value": ["patched-2"]
    }
    r = patch_resource(path, patch)
    print("PATCH returned:")
    images = r.json()
    pprint(images)
    print(f"{len(images['member'])} assets returned.")
    print()


if __name__ == '__main__':
    post_all_images_2025()
    get_all_images()
    get_all_images_with_query()
    # patch_all_images_with_query() not yet supported
    # patch_all_images_with_members() #  HTTP 400 "Unsupported field 'string2'"