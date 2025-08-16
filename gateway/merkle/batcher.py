import json, os, time, hashlib
from typing import List, Dict, Any, Tuple
from .merkle_tree import merkle_root, merkle_proof
from ..security.signer import device_sign, canonical_json
from ..storage.local_store import LocalStore

def hash_record(record: Dict[str, Any], device_secret: bytes) -> bytes:
    # Sign + canonicalize record => leaf bytes
    signed = device_sign(record, device_secret)
    payload = canonical_json({"record": record, "sig": signed.hex()})
    return payload.encode("utf-8")  # leaf material; merkle_tree will hash again

class MerkleBatcher:
    def __init__(self, store: LocalStore, window_size: int = 100):
        self.store = store
        self.window_size = window_size

    def build_batches(self, records: List[Dict[str, Any]], device_secret: bytes) -> List[Dict[str, Any]]:
        batches = []
        window = []
        for r in records:
            window.append(r)
            if len(window) >= self.window_size:
                batches.append(self._flush(window, device_secret))
                window = []
        if window:
            batches.append(self._flush(window, device_secret))
        return batches

    def _flush(self, batch_records: List[Dict[str, Any]], device_secret: bytes) -> Dict[str, Any]:
        leaves = [hash_record(r, device_secret) for r in batch_records]
        root = merkle_root(leaves)
        root_hex = root.hex()
        # compute proofs for each record and persist batch manifest
        manifest_items = []
        for i, r in enumerate(batch_records):
            root2, proof, idx = merkle_proof(leaves, i)
            assert root2 == root
            manifest_items.append({
                "record_id": r["record_id"],
                "leaf_index": idx,
                "proof": [p.hex() for p in proof]
            })
            # persist raw_record line for demo
            self.store.append_line("raw", r)
        manifest = {
            "ts": int(time.time()),
            "merkle_root_hex": root_hex,
            "count": len(batch_records),
            "items": manifest_items,
        }
        self.store.append_line("batches", manifest)
        return manifest
