import os, time, hashlib, random
from typing import Dict, Any
from ..storage.local_store import LocalStore

class BitcoinAnchor:
    """Stubbed anchoring class.
    In production, replace 'broadcast_anchor' with real bitcoind JSON-RPC or service.
    """
    def __init__(self, store: LocalStore):
        self.store = store

    def broadcast_anchor(self, merkle_root_hex: str) -> Dict[str, Any]:
        # Dummy txid: sha256(root + timestamp + rand)
        rnd = os.urandom(8)
        now = int(time.time()).to_bytes(8, 'big')
        txid = hashlib.sha256(bytes.fromhex(merkle_root_hex) + now + rnd).hexdigest()
        anchor = {
            "merkle_root_hex": merkle_root_hex,
            "txid": txid,
            "first_seen": int(time.time()),
            "block_hash": None,
            "block_height": None,
            "confirmations": 0,
        }
        self.store.upsert_anchor(anchor)
        return anchor

    def mark_confirmed(self, merkle_root_hex: str, block_height: int) -> Dict[str, Any]:
        # Simulate confirmation by assigning a fake block_hash and incrementing confs
        anchor = self.store.get_anchor(merkle_root_hex)
        if not anchor:
            raise ValueError("Anchor not found for root" )
        fake_block_hash = hashlib.sha256((anchor["txid"] + str(block_height)).encode()).hexdigest()
        anchor.update({
            "block_hash": fake_block_hash,
            "block_height": block_height,
            "confirmations": max(anchor.get("confirmations", 0), 1),
        })
        self.store.upsert_anchor(anchor)
        return anchor
