from w3lib.url import canonicalize_url, url_query_cleaner
from hashlib import sha224
from urllib.parse import urlparse
from scutter import config
import os.path


def ensure_canonical_url(url):
    url = canonicalize_url(url)
    if "?" in url:
        remove_params = list(non_canonical_params(url))
        url = url_query_cleaner(url, remove_params, remove=True)
    return url


def non_canonical_params(url):
    for (domain, site) in config:
        if domain in url:
            yield from site.non_canonical_params
    yield from ["utm_campaign", "utm_medium", "utm_source"]


def get_url_hash(canonical_url: str):
    encoded_str = canonical_url.encode("utf-8")
    hex_digest = sha224(encoded_str).hexdigest()
    return hex_digest


def get_domain(url: str):
    return urlparse(url).netloc


def get_cache_fn(url, root="/tmp/atb"):
    canonical_url = ensure_canonical_url(url)
    hashed = get_url_hash(canonical_url)
    domain = get_domain(canonical_url)
    parts = [domain[0], domain] + list(hashed[:5]) + [hashed]
    return os.path.join(root, *parts)
