import hashlib, os

CACHE_DIR = ".bitscrapper_cache"

def get_cache_path(url: str) -> str:
    if not os.path.exists(CACHE_DIR):
        os.makedirs(CACHE_DIR)
    filename = hashlib.md5(url.encode('utf-8')).hexdigest()
    return os.path.join(CACHE_DIR, f"{filename}.html")

def load_from_cache(url: str) -> str | None:
    path = get_cache_path(url)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as file:
            return file.read()
    return None

def save_to_cache(url: str, content: str) -> None:
    path = get_cache_path(url)
    with open(path, 'w', encoding='utf-8') as file:
        file.write(content)