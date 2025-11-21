import io
from PIL import Image
import hashlib
from cachetools import TTLCache
from fastapi import HTTPException

# Simple in-memory cache: image_hash -> result
# TTL 24 hours, max 200 entries; for production replace with Redis
cache = TTLCache(maxsize=200, ttl=60*60*24)

def validate_image_bytes(b: bytes):
    try:
        Image.open(io.BytesIO(b)).verify()
        return True
    except Exception:
        return False

def image_hash(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def get_cached(hash_key: str):
    return cache.get(hash_key)

def set_cached(hash_key: str, value):
    cache[hash_key] = value
