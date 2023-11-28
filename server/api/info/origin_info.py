import requests

from entities.website_update import WebsiteUpdate
from ..configs import base_url, headers
from ..throw_api_error import _throw_api_error


def get_origin_info(origin: str) -> WebsiteUpdate:
    url = f"{base_url}/info/get/{origin}"

    response = requests.get(url, headers=headers)

    if response.status_code == 404:
        return None

    results = response.json()

    if response.status_code != 200:
        _throw_api_error(results)

    return WebsiteUpdate(
        origin=results["data"]["origin"],
        language=results["data"]["language"],
        populars=results["data"]["populars"],
    )


def origin_exists(origin: str) -> bool:
    url = f"{base_url}/info/get/{origin}"

    response = requests.get(url, headers=headers)
    results = response.json()

    if response.status_code == 404:
        return False

    if response.status_code != 200:
        _throw_api_error(results)

    return results["data"] != None


def update_info(info: WebsiteUpdate) -> bool:
    url = f"{base_url}/info/update"

    response = requests.post(url, json=info.to_dict(), headers=headers)
    results = response.json()

    if response.status_code != 200:
        _throw_api_error(results)

    return results["data"]


def add_info(info: WebsiteUpdate) -> bool:
    url = f"{base_url}/info/add"

    response = requests.post(url, json=info.to_dict(), headers=headers)
    results = response.json()

    if response.status_code != 200:
        _throw_api_error(results)

    return results["data"] != None
