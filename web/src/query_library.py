import json
from pathlib import Path
from typing import Dict

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
QUERY_FILE = DATA_DIR / 'queries.json'


def load_queries() -> Dict[str, Dict[str, str]]:
    if QUERY_FILE.exists():
        with open(QUERY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"shodan": {}, "censys": {}, "wigle": {}}


def save_query(service: str, name: str, query: str) -> None:
    data = load_queries()
    service_dict = data.setdefault(service, {})
    service_dict[name] = query
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(QUERY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)


def get_query(service: str, name: str) -> str:
    data = load_queries()
    return data.get(service, {}).get(name, '')


def list_queries(service: str) -> Dict[str, str]:
    data = load_queries()
    return data.get(service, {})
