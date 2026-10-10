# JUDGE START HERE — VELQIRIS × NEBIUS × NVIDIA NEMOTRON AGENT
**Hackathon:** Nebius x NVIDIA Global AI Hackathon (Devpost #1225763)  
**Track:** Agentic Engineering & Financial Reasoning  
**Verification Time:** < 5 seconds  

---

## 1. What Is This Project?
An institutional quantitative agent that uses high-throughput NVIDIA Nemotron LLM inference hosted on the Nebius Token Factory cloud to perform structured microstructure reasoning over multi-venue orderbook telemetry. Adheres strictly to a **Fail-Closed Policy**: zero ungrounded simulation or hallucination if credentials are unset.

---

## 2. Quick Verification

### A. Local Invariant & Schema Verification (Zero Dependencies, Zero Cost)
```bash
# Run unit tests validating prompt schemas and fail-closed handling
python3 -m unittest -v test_nemotron_market_agent.py
```
Expected Output:
```
test_missing_key_fails_closed ... ok
test_missing_model_fails_closed ... ok
test_prompt_uses_supplied_telemetry ... ok

Ran 3 tests in 0.000s
OK
```

### B. Live Nebius Token Factory Cloud Evaluation (For Judges / Sponsors)
If you are evaluating this project with your sponsor or judge Nebius API key:
```bash
export NEBIUS_API_KEY="<your_nebius_api_key>"
export NEBIUS_MODEL="nvidia/nemotron-4-340b-instruct"
python3 nemotron_market_agent.py
```
The agent will execute live inference against `https://api.tokenfactory.nebius.com/v1/chat/completions`, validate structured JSON output, and record a cryptographic execution proof file in `nebius_verified_execution_proof.json`.

---

## 3. Key Deliverables & Documentation

- [Nebius Runtime Verification & Reasoning Report](./NEBIUS_RUNTIME_VERIFICATION.md)
- [Agent Implementation](./nemotron_market_agent.py)
- [Pre-Existing Technology Disclosure](./PREEXISTING_TECHNOLOGY.md)
- [Verification Evidence Log](./VERIFICATION_EVIDENCE.md)
