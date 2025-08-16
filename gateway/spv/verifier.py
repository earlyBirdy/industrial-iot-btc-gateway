from typing import Dict, Any
from .headers import HeadersDB

class SPVVerifier:
    """Toy SPV verifier that checks if an 'anchor' is confirmed by having a block height set
    and that our local headers DB is at or past that height.
    """
    def __init__(self, headers_db: HeadersDB):
        self.headers_db = headers_db

    def is_confirmed(self, anchor: Dict[str, Any]) -> bool:
        bh = anchor.get("block_height")
        if bh is None:
            return False
        tip = self.headers_db.tip()
        return tip and tip.get("height", -1) >= bh
