# Industrial IoT → Bitcoin Trusted Gateway (Starter)

This is a **starter repo** that demonstrates how an industrial IoT embedded computer can
act as a **trusted gateway** that provides **tamper-evident logging** by anchoring
batched sensor readings to the **Bitcoin** blockchain via **Merkle root commitments**.

> This is a minimal proof-of-concept; it is not production-ready. The anchoring and SPV
> modules are intentionally simple and provide stubbed behaviors to let you run locally.

---

## 🌟 Unique Value Proposition

Compared with other data-integrity solutions in the IoT/blockchain market, this gateway delivers:

1. **Bitcoin Anchoring = Highest Security & Neutrality**
   - Anchors only a 32-byte Merkle root into Bitcoin — the world’s most secure and longest-lived blockchain.
   - Unlike private or consortium blockchains, no vendor or authority can rewrite history.

2. **Lightweight Edge Deployment**
   - Runs on rugged industrial embedded PCs (Intel Atom, ARM, Sintrones, Advantech).
   - Uses SPV (headers-only) instead of full chain → small footprint.

3. **Privacy-Preserving**
   - All raw IoT data stays **off-chain**. Only cryptographic commitments are published.
   - Protects sensitive operational telemetry and intellectual property.

4. **Vendor Neutral & Globally Auditable**
   - Proofs can be verified by anyone using any Bitcoin node or block explorer.
   - Auditors, insurers, and regulators can independently check integrity.

5. **Low Operational Cost**
   - By batching millions of records into one Merkle root, anchoring cost per record is **fractions of a cent**.
   - Much cheaper than storing raw data on Ethereum or paying enterprise SaaS fees.

6. **Seamless OT/IT Integration**
   - Designed for MQTT, OPC-UA, Modbus, and other industrial protocols.
   - Adds security as a **layer**, without replacing existing SCADA/ERP systems.

---

## 📊 Comparison with Other Solutions

| Feature            | Industrial-IoT-BTC-Gateway        | Private Blockchain (Hyperledger) | Ethereum / Alt L1s       | SaaS Vendor Logging   |
|--------------------|-----------------------------------|----------------------------------|--------------------------|-----------------------|
| **Security**       | Anchored in Bitcoin (strongest PoW) | Consortium trust (rewrite possible) | Strong but costly gas, central infra risk | Vendor-controlled |
| **Cost per record**| Tiny (Merkle batching)            | Moderate infra/licensing costs   | High gas fees per tx      | Subscription fees     |
| **Privacy**        | Raw data off-chain, only hashes   | Depends on setup                | Public by default         | Vendor holds raw data |
| **Footprint**      | Lightweight (SPV only)            | Heavy infra nodes                | Requires wallet + RPC     | Cloud-only dependency |
| **Auditability**   | Global, neutral, public           | Limited to consortium members    | Public, but expensive     | Must trust vendor     |
| **OT/IT Fit**      | Native protocols, edge-ready      | Needs middleware & connectors    | Needs bridges/APIs        | API-only integrations |

---

## 🏭 Mapped Industrial Use Case

**Predictive Maintenance & Compliance in a Factory**

- **Problem**: Factories need to track vibration, temperature, and energy data from machines to prevent downtime and to prove compliance with ISO/IEC standards. Traditional logs can be tampered with by internal staff or lost due to system failures.  
- **Solution with Gateway**:  
  - Each IoT record (sensor reading) is signed by the device.  
  - Batches are hashed → Merkle root → anchored on Bitcoin every 5 minutes.  
  - Auditors/regulators later verify that machine condition logs are untampered, using public blockchain proofs.  
- **Impact**:  
  - Strong evidence in warranty disputes (proves machine was overheated before delivery).  
  - Meets compliance requirements for safety-critical industries (aerospace, pharma, automotive).  
  - Reduces fraud risk in SLA/contract claims.

---

## 💰 Clear ROI vs Alternatives

- **Bitcoin Anchoring (this gateway)**  
  - ~$5–10 per day (if batching every 5 minutes, 288 anchors/day at ~10–30 sat/vB fees).  
  - Cost per record → fractions of a cent, even with millions of sensor points.  
  - Immutable, neutral, vendor-independent proofs.  

- **Private Blockchain (Hyperledger, etc.)**  
  - Requires operating a consortium, infra overhead (nodes, CA, governance).  
  - Cost → $50k–$200k per year for infra + staff.  
  - Security depends on consortium honesty.

- **Ethereum / Alt L1 anchoring**  
  - Gas costs can be $0.50–$5 per tx (volatile).  
  - High cost per anchor makes frequent logging impractical.  
  - Public but pricing is unpredictable.

- **SaaS Logging (Splunk, Azure IoT, AWS IoT)**  
  - Subscription + data ingestion costs scale with volume.  
  - $10k–$100k/year for medium deployments.  
  - Auditability limited: auditors must trust vendor reports.  

**ROI Summary**:  
➡️ The Industrial-IoT-BTC-Gateway is **10–100x cheaper** than SaaS/enterprise blockchains while providing **stronger audit guarantees** (Bitcoin immutability). Perfect for industries where **compliance, warranty, and safety logs** are mission-critical.

---

## Quick start

### 1) Create a virtual environment (optional)
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Run the gateway (build batches + anchor)
```bash
python scripts/run_gateway.py --input examples/sample_data.json --window 10
```

### 3) Verify a single record (Merkle proof + anchor lookup)
```bash
python scripts/verify_record.py --record-id devA:0005
```

---

**DISCLAIMER**: Educational sample only; no warranties. Use at your own risk.
