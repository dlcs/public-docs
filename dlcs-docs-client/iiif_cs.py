import base64
import json

import requests
import settings

def basic_auth_header():
    return  {
        "Authorization": f"Basic {base64.b64encode(settings.IIIF_CS_BASIC_CREDENTIALS.encode("utf-8")).decode("ascii")}"
    }

def send_headers():
    return {
        "Authorization": f"Basic {base64.b64encode(settings.IIIF_CS_BASIC_CREDENTIALS.encode("utf-8")).decode("ascii")}",
        "Content-Type": "application/json",
    }


def normalise_path(path):
    if path.startswith("http"):
        return path

    if path[0] != '/':
        path = '/' + path

    return f"{settings.IIIF_CS_API_HOST}{path}"


def get_resource(path: str):
    np = normalise_path(path)
    r = requests.get(np, headers=basic_auth_header())
    return r


def pprint(json_as_dict):
    print(json.dumps(json_as_dict, indent=4))