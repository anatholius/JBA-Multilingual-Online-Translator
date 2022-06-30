import requests


def check_success(url):
    return 'Success' if requests.get(url) else 'Fail'
