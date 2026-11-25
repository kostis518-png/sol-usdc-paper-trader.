import os
import unittest
from unittest.mock import patch

from security_gate import (
    ApprovalContext,
    OperatingMode,
    SecurityGateError,
    assert_broadcast_allowed,
    assert_signing_allowed,
    configured_mode,
)


class SecurityGateTests(unittest.TestCase):
    def valid_devnet(self, **overrides):
        values = dict(
            mode=OperatingMode.DEVNET,
            network="devnet",
            initiated_by_user=True,
            source="user",
            simulation_passed=True,
            phantom_approved=True,
            execution_confirmed=True,
        )
        values.update(overrides)
        return ApprovalContext(**values)

    def test_default_mode_is_paper(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(configured_mode(), OperatingMode.PAPER)

    def test_invalid_mode_fails_closed_to_paper(self):
        with patch.dict(os.environ, {"TRADING_MODE": "LIVE"}, clear=True):
            self.assertEqual(configured_mode(), OperatingMode.PAPER)

    def test_paper_broadcast_is_blocked(self):
        ctx = self.valid_devnet(mode=OperatingMode.PAPER, network="devnet")
        with self.assertRaises(SecurityGateError):
            assert_broadcast_allowed(ctx)

    def test_strategy_signal_cannot_authorize_signing(self):
        ctx = self.valid_devnet(source="strategy", initiated_by_user=False)
        with self.assertRaises(SecurityGateError):
            assert_signing_allowed(ctx)

    def test_signing_requires_simulation(self):
        with self.assertRaises(SecurityGateError):
            assert_signing_allowed(self.valid_devnet(simulation_passed=False))

    def test_signing_requires_phantom_approval(self):
        with self.assertRaises(SecurityGateError):
            assert_signing_allowed(self.valid_devnet(phantom_approved=False))

    def test_signing_is_devnet_only(self):
        with self.assertRaises(SecurityGateError):
            assert_signing_allowed(self.valid_devnet(mode=OperatingMode.MAINNET, network="mainnet-beta"))

    def test_devnet_signing_gate_accepts_complete_user_flow(self):
        assert_signing_allowed(self.valid_devnet())

    def test_broadcast_requires_separate_execution_confirmation(self):
        with self.assertRaises(SecurityGateError):
            assert_broadcast_allowed(self.valid_devnet(execution_confirmed=False))

    def test_mainnet_broadcast_blocked_by_default(self):
        ctx = self.valid_devnet(mode=OperatingMode.MAINNET, network="mainnet-beta")
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(SecurityGateError, "disabled"):
                assert_broadcast_allowed(ctx)

    def test_mainnet_remains_unimplemented_even_when_flagged(self):
        ctx = self.valid_devnet(mode=OperatingMode.MAINNET, network="mainnet-beta")
        with patch.dict(os.environ, {"MAINNET_BROADCAST_ENABLED": "true"}, clear=True):
            with self.assertRaisesRegex(SecurityGateError, "not implemented"):
                assert_broadcast_allowed(ctx)

    def test_devnet_broadcast_gate_requires_correct_network(self):
        with self.assertRaises(SecurityGateError):
            assert_broadcast_allowed(self.valid_devnet(network="mainnet-beta"))


if __name__ == "__main__":
    unittest.main()
