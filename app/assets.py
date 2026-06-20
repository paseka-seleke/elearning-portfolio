"""
Content-hash cache busting for static assets.

A short hash of the file's actual bytes, used as a `?v=` query string. Because
the hash only changes when the file's content changes, it is safe to tell
browsers to cache /static/* responses forever (see the Cache-Control
middleware in main.py): the URL itself changes whenever the content does, so
there is no stale-cache risk, and repeat visits skip re-downloading anything
that hasn't changed.
"""
import hashlib
from functools import lru_cache
from pathlib import Path

STATIC_DIR = Path(__file__).resolve().parent / "static"


@lru_cache(maxsize=None)
def asset_version(rel_path: str) -> str:
    file_path = STATIC_DIR / rel_path
    try:
        data = file_path.read_bytes()
    except FileNotFoundError:
        return "0"
    return hashlib.sha1(data).hexdigest()[:8]
