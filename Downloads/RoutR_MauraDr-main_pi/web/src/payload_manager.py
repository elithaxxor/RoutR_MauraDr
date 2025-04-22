import os
import yaml
from typing import List, Dict, Any, Optional

class Payload:
    def __init__(self, path: str, metadata: Dict[str, Any], content: str):
        self.path = path
        self.metadata = metadata
        self.content = content

    def matches(self, vendor: Optional[str]=None, model: Optional[str]=None, firmware: Optional[str]=None) -> bool:
        meta = self.metadata
        if vendor and meta.get('vendor', '').lower() != vendor.lower():
            return False
        if model and meta.get('model', '').lower() != model.lower():
            return False
        if firmware and meta.get('firmware', '').lower() != firmware.lower():
            return False
        return True

class PayloadManager:
    def __init__(self, payloads_dir: str = '../../payloads'):
        self.payloads_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), payloads_dir))
        self.payloads: List[Payload] = []
        self._load_payloads()

    def _load_payloads(self):
        for root, _, files in os.walk(self.payloads_dir):
            for file in files:
                if file.endswith(('.md', '.py', '.txt', '.http')):
                    full_path = os.path.join(root, file)
                    with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    metadata, body = self._parse_metadata(content)
                    self.payloads.append(Payload(full_path, metadata, body))

    def _parse_metadata(self, content: str) -> (Dict[str, Any], str):
        if content.startswith('---'):
            end = content.find('---', 3)
            if end != -1:
                meta_str = content[3:end]
                try:
                    metadata = yaml.safe_load(meta_str)
                except Exception:
                    metadata = {}
                return metadata or {}, content[end+3:].lstrip('\n')
        return {}, content

    def list_payloads(self, vendor: Optional[str]=None, model: Optional[str]=None, firmware: Optional[str]=None) -> List[Payload]:
        return [p for p in self.payloads if p.matches(vendor, model, firmware)]

    def get_payload(self, path: str) -> Optional[Payload]:
        for p in self.payloads:
            if p.path == path:
                return p
        return None

    def search_payloads(self, query: str) -> List[Payload]:
        query = query.lower()
        return [p for p in self.payloads if query in p.content.lower() or any(query in str(v).lower() for v in p.metadata.values())]

    def all_payloads(self) -> List[Payload]:
        return self.payloads
