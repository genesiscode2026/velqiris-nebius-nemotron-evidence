# VELQIRIS Nemotron Evidence Agent

An evidence-controlled market-risk reasoning client for the Nebius × NVIDIA Global AI Hackathon.

The client calls an NVIDIA Nemotron model through Nebius Token Factory only when both `NEBIUS_API_KEY` and an exact model identifier from the live Token Factory catalogue are configured. Without either value it fails closed and explicitly records that no cloud execution occurred.

## Run

```bash
export NEBIUS_API_KEY='...'
export NEBIUS_MODEL='exact-model-id-from-the-live-token-factory-catalogue'
python3 nemotron_market_agent.py
```

The default API base is `https://api.tokenfactory.nebius.com/v1`; it can be changed with `NEBIUS_BASE_URL`. No historical model identifier is hard-coded or presented as currently available.

## Submission gate

The official competition requires a real runtime call on Nebius and a working public demo. This repository is not submission-complete until a redacted execution proof exists and the demo uses actual Token Factory output.

## License

MIT.
