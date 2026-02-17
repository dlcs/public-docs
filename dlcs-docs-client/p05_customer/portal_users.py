import settings
from iiif_cs import get_cloud_services_resource, post_resource, pprint, delete_resource


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


if __name__ == '__main__':
    get_portal_users()
    new_user = post_portal_user()
    get_portal_users()
    delete_resource(new_user['@id'])