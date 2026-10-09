# JUDGE START HERE — VELQIRIS × NEBIUS × NVIDIA NEMOTRON AGENT
**Hackathon:** Nebius x NVIDIA Global AI Hackathon (Devpost #1225763)  
**Track:** Agentic Engineering & Financial Reasoning  
**Verification Time:** < 5 seconds  

---

## 1. What Is This Project?
An institutional quantitative agent that uses high-throughput NVIDIA Nemotron LLM inference hosted on the Nebius Token Factory cloud to perform structured microstructure reasoning over multi-venue orderbook telemetry. Adheres strictly to a **Fail-Closed Policy**: zero ungrounded simulation or hallucination if credentials are unset.

---

## 2. Quick Verification (Run in 1 Command)

```bash
# Run unit tests validating prompt schemas and fail-closed handling
python3 -m unittest -v test_nemotron_market_agent.py
```

### Expected Output:
```
test_missing_key_fails_closed ... ok
test_missing_model_fails_closed ... ok
test_prompt_uses_supplied_telemetry ... ok

Ran 3 tests in 0.000s
OK
```

---

## 3. Key Deliverables & Documentation

- [Nebius Runtime Verification & Reasoning Report](./NEBIUS_RUNTIME_VERIFICATION.md)
- [Agent Implementation](./nemotron_market_agent.py)
- [Pre-Existing Technology Disclosure](./PREEXISTING_TECHNOLOGY.md)
- [Verification Evidence Log](./VERIFICATION_EVIDENCE.md)
