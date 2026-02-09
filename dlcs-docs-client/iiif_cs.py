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