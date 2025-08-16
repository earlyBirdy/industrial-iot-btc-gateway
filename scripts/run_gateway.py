import argparse, json, os, time
from typing import List, Dict, Any
from gateway.storage.local_store import LocalStore
from gateway.merkle.batcher import MerkleBatcher
from gateway.anchor.bitcoin_anchor import BitcoinAnchor
from gateway.spv.headers import HeadersDB

DEVICE_SECRET = b"demo-device-secret"  # replace with TPM/HSM usage in production

def load_records(path: str) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="Path to JSON array of records")
    ap.add_argument("--window", type=int, default=10, help="Records per batch window (demo)")
    args = ap.parse_args()

    store = LocalStore()
    batcher = MerkleBatcher(store=store, window_size=args.window)
    records = load_records(args.input)
    print(f"Loaded {len(records)} records from {args.input}")

    batches = batcher.build_batches(records, DEVICE_SECRET)
    print(f"Created {len(batches)} batches.")

    anchor = BitcoinAnchor(store)
    headers = HeadersDB()
    for b in batches:
        root = b["merkle_root_hex"]
        a = anchor.broadcast_anchor(root)
        print(f"Anchored root {root} with txid {a['txid']}")
        # simulate a few confirmations by growing headers and then marking as confirmed
        headers.grow_chain(1)
        tip = headers.tip()
        a2 = anchor.mark_confirmed(root, block_height=tip["height"])
        print(f"Batch at root {root} confirmed at height {a2['block_height']}")

if __name__ == "__main__":
    main()
