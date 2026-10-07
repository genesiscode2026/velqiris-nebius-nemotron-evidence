import unittest

from nemotron_market_agent import NemotronMarketReasoningAgent


class NemotronAgentTests(unittest.TestCase):
    def test_missing_key_fails_closed(self):
        result = NemotronMarketReasoningAgent(api_key='', model='nvidia/example').reason_over_market_data({'symbol': 'BTC'})
        self.assertEqual(result['status'], 'BLOCKED_AWAITING_NEBIUS_CONFIGURATION')
        self.assertFalse(result['cloud_api_invoked'])

    def test_missing_model_fails_closed(self):
        result = NemotronMarketReasoningAgent(api_key='x', model='').reason_over_market_data({'symbol': 'BTC'})
        self.assertEqual(result['status'], 'BLOCKED_AWAITING_NEBIUS_CONFIGURATION')
        self.assertIn('NEBIUS_MODEL', result['missing'])

    def test_prompt_uses_supplied_telemetry(self):
        messages = NemotronMarketReasoningAgent(api_key='x', model='nvidia/example').build_structured_prompt({
            'symbol': 'ETH',
            'byzantine_median_price_usd': 1234.5,
            'spread_basis_points': 1.2,
            'data_trust_score': 97,
        })
        self.assertIn('ETH', messages[1]['content'])
        self.assertIn('1,234.50', messages[1]['content'])
        self.assertIn('1.2 bps', messages[1]['content'])


if __name__ == '__main__':
    unittest.main()
