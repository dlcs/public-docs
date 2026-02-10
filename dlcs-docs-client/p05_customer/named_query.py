import settings
from iiif_cs import get_cloud_services_resource, post_resource, pprint


def get_named_queries():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/namedQueries"
    named_queries = get_cloud_services_resource(path).json()
    print("GET returned:")
    pprint(named_queries)
    print()


def post_named_query():
    path = f"/customers/{settings.IIIF_CS_CUSTOMER_ID}/namedQueries"
    named_query = {
        "name": "manifest-from-space",
        "template": "manifest=s1&sequence=0&canvas=n1&s1=p1"
    }
    r = post_resource(path, named_query)
    print("POST returned:")
    pprint(r.json())
    print()


if __name__ == '__main__':
    get_named_queries()
    # post_named_query()