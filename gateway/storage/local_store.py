import json
import os
from typing import Dict, Any, List, Optional

class LocalStore:
    """
    Tiny JSON-file based storage to keep demo state:
    - raw_records.jsonl
    - batches.jsonl
    - anchors.jsonl
    """
    def __init__(self, base_dir: str = ".data"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)
        self._files = {
            "raw": os.path.join(self.base_dir, "raw_records.jsonl"),
            "batches": os.path.join(self.base_dir, "batches.jsonl"),
            "anchors": os.path.join(self.base_dir, "anchors.jsonl"),
        }

    def append_line(self, name: str, obj: Dict[str, Any]) -> None:
        path = self._files[name]
        with open(path, "a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")

    def read_all(self, name: str) -> List[Dict[str, Any]]:
        path = self._files[name]
        if not os.path.exists(path):
            return []
        out = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                out.append(json.loads(line))
        return out

    def find_batch_by_root(self, merkle_root_hex: str) -> Optional[Dict[str, Any]]:
        for b in self.read_all("batches"):
            if b.get("merkle_root_hex") == merkle_root_hex:
                return b
        return None

    def upsert_anchor(self, anchor: Dict[str, Any]) -> None:
        # naive upsert for demo: rewrite anchors file
        anchors = self.read_all("anchors")
        found = False
        for i, a in enumerate(anchors):
            if a.get("merkle_root_hex") == anchor.get("merkle_root_hex"):
                anchors[i] = anchor
                found = True
                break
        if not found:
            anchors.append(anchor)
        path = self._files["anchors"]
        with open(path, "w", encoding="utf-8") as f:
            for a in anchors:
                f.write(json.dumps(a, ensure_ascii=False) + "\n")

    def get_anchor(self, merkle_root_hex: str) -> Optional[Dict[str, Any]]:
        for a in self.read_all("anchors"):
            if a.get("merkle_root_hex") == merkle_root_hex:
                return a
        return None
