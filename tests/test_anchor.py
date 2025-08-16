from gateway.storage.local_store import LocalStore
from gateway.anchor.bitcoin_anchor import BitcoinAnchor

def test_anchor_cycle():
    store = LocalStore(base_dir=".data/teststore")
    anc = BitcoinAnchor(store)
    root = "a"*64
    a = anc.broadcast_anchor(root)
    assert a["txid"]
    a2 = anc.mark_confirmed(root, block_height=100)
    assert a2["block_height"] == 100
