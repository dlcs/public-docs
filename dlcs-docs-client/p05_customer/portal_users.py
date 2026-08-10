import settings
from iiif_cs import get_cloud_services_resource, post_resource, patch_resource, pprint, delete_resource

# NOTE: portal user accounts will be deprecated - the current customer portal
# manages its users externally. These operations remain for existing integrations.


def get_portal_users():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/portalUsers"
    portal_users = get_cloud_services_resource(path).json()
    print("GET returned:")
    pprint(portal_users)
    print()


def post_portal_user():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/portalUsers"
    portal_user = {
        "email": "user@example.com",
        "password": "plaintext-password" # sent once only, not retrievable
    }
    r = post_resource(path, portal_user)
    portal_user = r.json()
    print("POST returned:")
    pprint(portal_user)
    print()
    return portal_user


def get_portal_user(portal_user_url):
    portal_user = get_cloud_services_resource(portal_user_url).json()
    print("GET single portal user returned:")
    pprint(portal_user)
    print()
    return portal_user


def patch_portal_user(portal_user_url):
    # Only email and password can be changed; `enabled` cannot be toggled via the API
    updates = {
        "email": "renamed-user@example.com"
    }
    r = patch_resource(portal_user_url, updates)
    portal_user = r.json()
    print("PATCH returned:")
    pprint(portal_user)
    print()
    return portal_user


if __name__ == '__main__':
    get_portal_users()
    new_user = post_portal_user()
    get_portal_user(new_user['@id'])
    patch_portal_user(new_user['@id'])
    get_portal_users()
    delete_resource(new_user['@id'])
