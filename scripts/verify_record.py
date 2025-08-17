import argparse, json
from typing import Dict, Any, List
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gateway.storage.local_store import LocalStore
from gateway.merkle.merkle_tree import verify_merkle_proof, sha256
from gateway.anchor.bitcoin_anchor import BitcoinAnchor
from gateway.spv.headers import HeadersDB
from gateway.spv.verifier import SPVVerifier

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--record-id", required=True, help="Record ID to verify (e.g., devA:0005)")
    args = ap.parse_args()

    store = LocalStore()
    batches = store.read_all("batches")
    raw = store.read_all("raw")

    # find the record's batch manifest item
    found_batch = None
    found_item = None
    for b in batches:
        for it in b.get("items", []):
            if it.get("record_id") == args.record_id:
                found_batch = b
                found_item = it
                break
        if found_item:
            break

    if not found_item:
        print("Record not found in any batch manifest.")
        return

    # locate the raw record content
    raw_record = None
    for r in raw:
        if r.get("record_id") == args.record_id:
            raw_record = r
            break

    if not raw_record:
        print("Raw record not found.")
        return

    # Rebuild the leaf payload as in batcher.hash_record()
    import hmac, hashlib, json as _json
    from gateway.security.signer import canonical_json
    DEVICE_SECRET = b"demo-device-secret"
    signed = hmac.new(DEVICE_SECRET, canonical_json(raw_record).encode("utf-8"), hashlib.sha256).digest()
    leaf_payload = canonical_json({"record": raw_record, "sig": signed.hex()}).encode("utf-8")

    proof = [bytes.fromhex(p) for p in found_item["proof"]]
    index = int(found_item["leaf_index"])
    root_hex = found_batch["merkle_root_hex"]
    ok = verify_merkle_proof(leaf_payload, proof, index, bytes.fromhex(root_hex))

    print("=== Merkle Proof ===")
    print(f"Record ID: {args.record_id}")
    print(f"Batch Root: {root_hex}")
    print(f"Leaf index: {index}")
    print(f"Proof len: {len(proof)}" )
    print(f"Proof valid: {ok}")

    print("\n=== Anchor & SPV ===")
    anchor = store.get_anchor(root_hex)
    if not anchor:
        print("Anchor not found for this root.")
        return
    print(f"txid: {anchor['txid']}")
    print(f"block_height: {anchor['block_height']}  confirmations: {anchor.get('confirmations', 0)}")

    headers = HeadersDB()
    spv = SPVVerifier(headers)
    print(f"SPV says confirmed: {spv.is_confirmed(anchor)}")

if __name__ == "__main__":
    main()
