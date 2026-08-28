import base64
import json
import time

import requests
import settings

BASIC_AUTH_HEADER = {
    "Authorization": f"Basic {base64.b64encode(settings.IIIF_CS_BASIC_CREDENTIALS.encode("utf-8")).decode("ascii")}"
}

BASIC_AUTH_WITH_CONTENT_TYPE = {
    "Authorization": f"Basic {base64.b64encode(settings.IIIF_CS_BASIC_CREDENTIALS.encode("utf-8")).decode("ascii")}",
    "Content-Type": "application/json"
}


def normalise_path(path):
    if path.startswith("http"):
        return path

    if path[0] != '/':
        path = '/' + path

    return f"{settings.IIIF_CS_API_HOST}{path}"


def get_cloud_services_resource(path: str):
    np = normalise_path(path)
    print("-------------------------------------------")
    print(f"GET {np}")
    r = requests.get(np, headers=BASIC_AUTH_HEADER)
    print(f"HTTP Status Code: {r.status_code}")
    return r


def put_resource(path: str, resource: any):
    np = normalise_path(path)
    print("-------------------------------------------")
    print(f"PUT {np}")
    print(resource)
    r = requests.put(np, headers=BASIC_AUTH_WITH_CONTENT_TYPE, json=resource)
    print(f"HTTP Status Code: {r.status_code}")
    return r


def post_resource(path: str, resource: any):
    np = normalise_path(path)
    print("-------------------------------------------")
    print(f"POST {np}")
    print(resource)
    r = requests.post(np, headers=BASIC_AUTH_WITH_CONTENT_TYPE, json=resource)
    print(f"HTTP Status Code: {r.status_code}")
    return r


def patch_resource(path: str, resource: any):
    np = normalise_path(path)
    print("-------------------------------------------")
    print(f"PATCH {np}")
    print(resource)
    r = requests.patch(np, headers=BASIC_AUTH_WITH_CONTENT_TYPE, json=resource)
    print(f"HTTP Status Code: {r.status_code}")
    return r


def delete_resource(path: str):
    np = normalise_path(path)
    print("-------------------------------------------")
    print(f"DELETE {np}")
    r = requests.delete(np, headers=BASIC_AUTH_WITH_CONTENT_TYPE)
    print(f"HTTP Status Code: {r.status_code}")
    return r


# Keep polling the resource at path until the value of resource['field'] is the expected value
def wait_for_value(path: str, field: str, value: any, interval: int=1, retries: int=5):
    print(f"Polling {path} until for {field} == {value}")
    for i in range(retries):
        print(f"Attempt {i}")
        try:
            r = get_cloud_services_resource(path)
            resource = r.json()
            found_value = resource.get(field, None)
            if found_value == value:
                print(f"Returned value was expected {found_value}, will stop polling")
                return resource
            print(f"Returned value was {found_value}, waiting {interval} seconds.")
            time.sleep(interval)
        except Exception as e:
            print(e)
            return None

    print(f"Abandoning polling after {retries} retries")
    return None



def pprint(json_as_dict):
    print(json.dumps(json_as_dict, indent=4))

# ---------------------------------------------------------------------------
# IIIF Presentation API (Manifests and Collections)
#
# The IIIF Presentation API lives on a different host from the Cloud Services
# API (iiif.* rather than api.*) but takes the same credentials. Two extra
# conventions apply there:
#
#   * X-IIIF-CS-Show-Extras: All   asks for the "API view" of a resource (all the
#                                  extra properties) rather than the public IIIF.
#   * ETag / If-Match              GETs return an ETag; a PUT that UPDATES and a
#                                  DELETE must send it back as If-Match (else 412);
#                                  a PUT that CREATES must NOT send one (else 400).
# ---------------------------------------------------------------------------

PRESENTATION_HEADERS = {
    **BASIC_AUTH_HEADER,
    "X-IIIF-CS-Show-Extras": "All"
}


def normalise_iiif_path(path):
    if path.startswith("http"):
        return path

    if path[0] != '/':
        path = '/' + path

    return f"{settings.IIIF_CS_PRESENTATION_HOST}{path}"


def get_iiif_resource(path: str, extras: bool = True):
    """GET from the IIIF Presentation API. extras=False makes the request an
    ordinary IIIF client would make: no auth, no Show-Extras header."""
    np = normalise_iiif_path(path)
    headers = PRESENTATION_HEADERS if extras else {}
    print("-------------------------------------------")
    print(f"GET {np}" + ("" if extras else "   (public, no auth)"))
    r = requests.get(np, headers=headers, allow_redirects=False)
    print(f"HTTP Status Code: {r.status_code}")
    if "ETag" in r.headers:
        print(f"ETag: {r.headers['ETag']}")
    return r


def put_iiif_resource(path: str, resource: any, etag: str = None):
    """PUT to the IIIF Presentation API. Pass etag (from a previous GET) when
    updating an existing resource; leave it out when creating one."""
    np = normalise_iiif_path(path)
    headers = {**PRESENTATION_HEADERS, "Content-Type": "application/json"}
    if etag:
        headers["If-Match"] = etag
    print("-------------------------------------------")
    print(f"PUT {np}" + (f"   If-Match: {etag}" if etag else ""))
    print(resource)
    r = requests.put(np, headers=headers, json=resource)
    print(f"HTTP Status Code: {r.status_code}")
    return r


def post_iiif_resource(path: str, resource: any):
    np = normalise_iiif_path(path)
    headers = {**PRESENTATION_HEADERS, "Content-Type": "application/json"}
    print("-------------------------------------------")
    print(f"POST {np}")
    print(resource)
    r = requests.post(np, headers=headers, json=resource)
    print(f"HTTP Status Code: {r.status_code}")
    return r


def delete_iiif_resource(path: str, etag: str):
    """DELETE from the IIIF Presentation API; the ETag of the current version is required."""
    np = normalise_iiif_path(path)
    headers = {**PRESENTATION_HEADERS, "If-Match": etag}
    print("-------------------------------------------")
    print(f"DELETE {np}   If-Match: {etag}")
    r = requests.delete(np, headers=headers)
    print(f"HTTP Status Code: {r.status_code}")
    return r
