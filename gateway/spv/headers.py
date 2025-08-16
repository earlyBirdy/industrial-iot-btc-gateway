import os, json, hashlib, time
from typing import List, Dict, Any

class HeadersDB:
    """Very small toy headers DB. In production, store real headers."""
    def __init__(self, path: str = ".data/headers.jsonl"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            # create a fake genesis header for demo
            self.append_header({"height": 0, "hash": self._fake_hash("genesis"), "time": int(time.time())})

    def _fake_hash(self, s: str) -> str:
        return hashlib.sha256(s.encode()).hexdigest()

    def append_header(self, header: Dict[str, Any]) -> None:
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(header) + "\n")

    def all(self) -> List[Dict[str, Any]]:
        out = []
        if not os.path.exists(self.path):
            return out
        with open(self.path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    out.append(json.loads(line))
        return out

    def tip(self) -> Dict[str, Any]:
        h = self.all()
        return h[-1] if h else None

    def grow_chain(self, n: int = 6) -> List[Dict[str, Any]]:
        """Simulate n new headers to give 'confirmations' in the demo."""
        tip = self.tip()
        out = []
        for i in range(n):
            height = tip["height"] + 1
            hsh = self._fake_hash(f"block-{height}-{time.time()}" )
            hdr = {"height": height, "hash": hsh, "time": int(time.time())}
            self.append_header(hdr)
            tip = hdr
            out.append(hdr)
        return out
