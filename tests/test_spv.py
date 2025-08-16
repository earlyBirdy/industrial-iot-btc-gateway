from gateway.spv.headers import HeadersDB

def test_headers_grow():
    db = HeadersDB(path=".data/test_headers.jsonl")
    tip0 = db.tip()
    db.grow_chain(3)
    tip1 = db.tip()
    assert tip1["height"] >= tip0["height"] + 3
