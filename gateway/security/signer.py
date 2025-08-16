import hmac, hashlib, json
from typing import Dict, Any

def canonical_json(obj: Dict[str, Any]) -> str:
    return json.dumps(obj, separators=(",", ":"), sort_keys=True, ensure_ascii=False)

def device_sign(record: Dict[str, Any], device_secret: bytes) -> bytes:
    """HMAC-SHA256 stand-in for a device signature. Replace with TPM/HSM in production."""
    payload = canonical_json(record).encode("utf-8")
    return hmac.new(device_secret, payload, hashlib.sha256).digest()
