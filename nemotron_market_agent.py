#!/usr/bin/env python3
"""
VELQIRIS × NEBIUS × NVIDIA: NEMOTRON FINANCIAL REASONING AGENT
================================================================================
Target: Nebius × NVIDIA Global AI Hackathon (Track 1: Coding & Agentic Engineering)
Model: an NVIDIA Nemotron model selected from the live Nebius Token Factory
model catalogue.

HARD INVARIANT:
Zero simulation. If NEBIUS_API_KEY or NEBIUS_MODEL is missing, fail closed
rather than claiming Nemotron was executed.
When called with live key, records exact request/response evidence on disk.
================================================================================
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional

NEBIUS_API_KEY = os.environ.get("NEBIUS_API_KEY", "")
NEBIUS_BASE_URL = os.environ.get("NEBIUS_BASE_URL", "https://api.tokenfactory.nebius.com/v1").rstrip("/")
NEMOTRON_MODEL = os.environ.get("NEBIUS_MODEL", "").strip()

class NemotronMarketReasoningAgent:
    def __init__(self, api_key: str = NEBIUS_API_KEY, model: str = NEMOTRON_MODEL):
        self.api_key = api_key
        self.model = model

    def build_structured_prompt(self, telemetry: Dict[str, Any]) -> List[Dict[str, str]]:
        system_prompt = (
            "You are an institutional quantitative risk and market microstructure reasoning agent. "
            "Analyze the provided multi-venue Byzantine price consensus and orderbook depth metrics. "
            "Return a strictly valid JSON object with: { 'regime': str, 'confidence_score': float, "
            "'risk_factors': list, 'recommended_execution_bias': str, 'rationale': str }."
        )

        user_content = (
            f"Asset: {telemetry.get('symbol', 'BTC')}\n"
            f"Byzantine Median Price: ${telemetry.get('byzantine_median_price_usd', 0.0):,.2f}\n"
            f"Cross-Exchange Spread: {telemetry.get('spread_basis_points', 0.0)} bps\n"
            f"Data Trust Score: {telemetry.get('data_trust_score', 0)}/100\n"
            f"Venue Feeds Evaluated: Binance, Coinbase, OKX\n"
            "Evaluate structural continuation vs liquidity absorption."
        )

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content}
        ]

    def reason_over_market_data(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes live inference on Nebius Token Factory if NEBIUS_API_KEY is configured.
        Fails closed with BLOCKED_AWAITING_NEBIUS_API_KEY if credentials are missing.
        """
        messages = self.build_structured_prompt(telemetry)
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.2,
            "response_format": {"type": "json_object"}
        }

        if not self.api_key or not self.model:
            missing = []
            if not self.api_key:
                missing.append("NEBIUS_API_KEY")
            if not self.model:
                missing.append("NEBIUS_MODEL")
            return {
                "status": "BLOCKED_AWAITING_NEBIUS_CONFIGURATION",
                "cloud_api_invoked": False,
                "model_requested": self.model or None,
                "endpoint": f"{NEBIUS_BASE_URL}/chat/completions",
                "payload_ready": True,
                "constructed_prompt": messages,
                "missing": missing,
                "error": "Required Nebius configuration is missing. In accordance with the zero-simulation invariant, Nemotron execution cannot be claimed."
            }

        req_body = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{NEBIUS_BASE_URL}/chat/completions",
            data=req_body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "VELQIRIS-Nemotron-Agent/1.0"
            }
        )

        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                resp_text = resp.read().decode("utf-8")
                res = json.loads(resp_text)
                raw_content = res["choices"][0]["message"]["content"]
                parsed_reasoning = json.loads(raw_content)

                # Persist verified request/response audit evidence
                evidence = {
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
                    "endpoint": f"{NEBIUS_BASE_URL}/chat/completions",
                    "model": self.model,
                    "request_payload": payload,
                    "response_raw": res,
                    "parsed_reasoning": parsed_reasoning
                }
                proof_path = os.path.join(os.path.dirname(__file__), "nebius_verified_execution_proof.json")
                with open(proof_path, "w", encoding="utf-8") as f:
                    json.dump(evidence, f, indent=2)

                return {
                    "status": "VERIFIED_NEBIUS_CLOUD_EXECUTION",
                    "cloud_api_invoked": True,
                    "model": self.model,
                    "reasoning": parsed_reasoning,
                    "evidence_file": proof_path
                }
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8", errors="ignore")
            return {
                "status": "NEBIUS_API_ERROR",
                "http_status": e.code,
                "cloud_api_invoked": True,
                "error": err_body
            }
        except Exception as e:
            return {
                "status": "CONNECTION_FAILED",
                "cloud_api_invoked": False,
                "error": str(e)
            }

if __name__ == "__main__":
    agent = NemotronMarketReasoningAgent()
    sample_data = {
        "symbol": "BTC",
        "byzantine_median_price_usd": 83450.0,
        "spread_basis_points": 0.45,
        "data_trust_score": 98
    }
    result = agent.reason_over_market_data(sample_data)
    print(json.dumps(result, indent=2))
