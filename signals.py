import threading
import time

_lock = threading.Lock()
_store = {}


def publish(name, **values):
    """Called by drowsiness / lane / vehicle modules."""
    with _lock:
        _store[name] = {**values, "ts": time.time()}


def read(name, max_age=5.0):
    """Returns the latest values, or None if missing or too old."""
    with _lock:
        item = _store.get(name)
    if item is None or time.time() - item["ts"] > max_age:
        return None
    return item