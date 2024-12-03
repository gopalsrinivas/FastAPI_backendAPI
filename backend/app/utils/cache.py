import time

cache = {}


def get(key):
    if key in cache and cache[key]["expires"] > time.time():
        return cache[key]["data"]
    return None


def set(key, value, expiration=600):
    cache[key] = {"data": value, "expires": time.time() + expiration}
