"""Fail-closed approval gates for wallet signing and transaction broadcast.

This module does not construct, sign, or broadcast transactions. It only defines
policy checks for a future user-driven transaction flow.
"""
from dataclasses import dataclass
from enum import Enum
import os


class OperatingMode(str, Enum):
    PAPER = "PAPER"
    DEVNET = "DEVNET"
    MAINNET = "MAINNET"


class SecurityGateError(PermissionError):
    """Raised when an operation violates the transaction safety policy."""


@dataclass(frozen=True)
class ApprovalContext:
    mode: OperatingMode
    network: str
    initiated_by_user: bool = False
    source: str = "strategy"
    simulation_passed: bool = False
    phantom_approved: bool = False
    execution_confirmed: bool = False


def configured_mode() -> OperatingMode:
    """Read the mode, defaulting safely to PAPER for missing/invalid values."""
    raw = os.getenv("TRADING_MODE", "PAPER").upper()
    try:
        return OperatingMode(raw)
    except ValueError:
        return OperatingMode.PAPER


def mainnet_broadcast_enabled() -> bool:
    """Mainnet requires an explicit project-owner environment setting."""
    return os.getenv("MAINNET_BROADCAST_ENABLED", "").strip().lower() == "true"


def _require_user_flow(ctx: ApprovalContext) -> None:
    if not ctx.initiated_by_user or ctx.source != "user":
        raise SecurityGateError("A strategy signal or background process cannot authorize a transaction.")
    if not ctx.simulation_passed:
        raise SecurityGateError("A successful transaction simulation is required.")
    if not ctx.phantom_approved:
        raise SecurityGateError("Explicit Phantom wallet approval is required.")


def assert_signing_allowed(ctx: ApprovalContext) -> None:
    """Permit only user-initiated Devnet signing after simulation and Phantom approval."""
    if ctx.mode is not OperatingMode.DEVNET or ctx.network.lower() != "devnet":
        raise SecurityGateError("Wallet signing is restricted to Devnet in this release.")
    _require_user_flow(ctx)


def assert_broadcast_allowed(ctx: ApprovalContext) -> None:
    """Policy gate for a future broadcaster; no broadcaster is implemented here."""
    if ctx.mode is OperatingMode.PAPER:
        raise SecurityGateError("PAPER mode never permits transaction broadcasting.")
    _require_user_flow(ctx)
    if not ctx.execution_confirmed:
        raise SecurityGateError("A separate, fresh execution confirmation is required.")
    if ctx.mode is OperatingMode.DEVNET:
        if ctx.network.lower() != "devnet":
            raise SecurityGateError("DEVNET mode cannot broadcast to another network.")
        return
    if ctx.mode is OperatingMode.MAINNET:
        if ctx.network.lower() not in ("mainnet", "mainnet-beta"):
            raise SecurityGateError("MAINNET mode requires the Solana Mainnet network.")
        if not mainnet_broadcast_enabled():
            raise SecurityGateError("Mainnet broadcasting is disabled by project-owner configuration.")
        raise SecurityGateError("Mainnet transaction execution is not implemented in this release.")
    raise SecurityGateError("Unsupported operating mode.")
