import hashlib
from typing import List, Tuple

def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()

def _pairwise(iterable):
    a = iter(iterable)
    return zip(a, a)

def merkle_root(leaves: List[bytes]) -> bytes:
    """Compute a Bitcoin-style Merkle root (double-SHA256 on concatenated nodes).
    For simplicity, we use single SHA256 for leaves and then double for internal nodes.
    """
    if not leaves:
        return b""
    level = [sha256(l) for l in leaves]
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])  # Bitcoin duplicates last if odd
        next_level = []
        for a, b in _pairwise(level):
            next_level.append(sha256(a + b))
        level = next_level
    return level[0]

def merkle_proof(leaves: List[bytes], index: int) -> Tuple[bytes, List[bytes], int]:
    """Return (root, proof_siblings, index) for the leaf at 'index'.
    Duplicates last node on odd levels (Bitcoin convention).
    """
    if not leaves:
        raise ValueError("no leaves")
    if index < 0 or index >= len(leaves):
        raise IndexError("leaf index out of range")
    level = [sha256(l) for l in leaves]
    proof = []
    idx = index
    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])
        next_level = []
        for i in range(0, len(level), 2):
            a = level[i]
            b = level[i+1]
            if i == idx ^ 1 or i == idx:
                # sibling for idx
                if i == idx:
                    proof.append(b)
                elif i+1 == idx:
                    proof.append(a)
            next_level.append(sha256(a + b))
        idx //= 2
        level = next_level
    return level[0], proof, index

def verify_merkle_proof(leaf: bytes, proof: List[bytes], index: int, expected_root: bytes) -> bool:
    h = sha256(leaf)
    idx = index
    for sib in proof:
        if idx % 2 == 0:
            h = sha256(h + sib)
        else:
            h = sha256(sib + h)
        idx //= 2
    return h == expected_root
