from gateway.merkle.merkle_tree import merkle_root, merkle_proof, verify_merkle_proof

def test_merkle_roundtrip():
    leaves = [f"leaf-{i}".encode() for i in range(5)]
    root = merkle_root(leaves)
    for i in range(len(leaves)):
        r, proof, idx = merkle_proof(leaves, i)
        assert r == root
        assert verify_merkle_proof(leaves[i], proof, idx, root)
