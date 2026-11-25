import { useEffect, useMemo, useState } from "react";
import { ConnectButton, useAccounts, useDisconnect, usePhantom } from "@phantom/react-sdk";
import { Connection, PublicKey, LAMPORTS_PER_SOL } from "@solana/web3.js";
import { getAssociatedTokenAddress } from "@solana/spl-token";

const RPC = "https://api.devnet.solana.com";
const DEVNET_USDC_MINT = "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU";
const BINANCE = "https://data-api.binance.vision";
const connection = new Connection(RPC, "confirmed");

type Balances = { sol: number; usdc: number };

function shortAddress(value: string) {
  return value.length > 12 ? value.slice(0, 5) + "…" + value.slice(-5) : value;
}

export default function App() {
  const { isConnected, isLoading } = usePhantom();
  const accounts = useAccounts();
  const { disconnect, isDisconnecting } = useDisconnect();
  const account = accounts?.find((item) => item.addressType === "solana");
  const address = account?.address ?? "";
  const [balances, setBalances] = useState<Balances | null>(null);
  const [balanceError, setBalanceError] = useState("");
  const [price, setPrice] = useState<number | null>(null);
  const [priceError, setPriceError] = useState("");
  const [refreshing, setRefreshing] = useState(false);

  const walletKey = useMemo(() => {
    try { return address ? new PublicKey(address) : null; }
    catch { return null; }
  }, [address]);

  async function refreshBalances() {
    if (!walletKey) return;
    setRefreshing(true);
    setBalanceError("");
    try {
      const [lamports, ata] = await Promise.all([
        connection.getBalance(walletKey, "confirmed"),
        getAssociatedTokenAddress(new PublicKey(DEVNET_USDC_MINT), walletKey, false),
      ]);
      let usdc = 0;
      try {
        const token = await connection.getTokenAccountBalance(ata, "confirmed");
        usdc = Number(token.value.uiAmount ?? 0);
      } catch (error) {
        // An absent associated token account means zero token balance.
        const message = error instanceof Error ? error.message : "";
        if (!message.toLowerCase().includes("could not find account") &&
            !message.toLowerCase().includes("accountnotfound")) throw error;
      }
      setBalances({ sol: lamports / LAMPORTS_PER_SOL, usdc });
    } catch (error) {
      setBalanceError(error instanceof Error ? error.message : "Balance retrieval failed.");
      setBalances(null);
    } finally {
      setRefreshing(false);
    }
  }

  async function refreshPrice() {
    setPriceError("");
    try {
      const response = await fetch(`${BINANCE}/api/v3/ticker/price?symbol=SOLUSDC`);
      if (!response.ok) throw new Error(`Binance returned HTTP ${response.status}`);
      const data: { symbol: string; price: string } = await response.json();
      if (data.symbol !== "SOLUSDC") throw new Error("Unexpected market symbol; refusing substitution.");
      setPrice(Number(data.price));
    } catch (error) {
      setPriceError(error instanceof Error ? error.message : "Market data unavailable.");
      setPrice(null);
    }
  }

  useEffect(() => { void refreshPrice(); }, []);
  useEffect(() => {
    if (walletKey) void refreshBalances();
    else { setBalances(null); setBalanceError(""); }
  }, [walletKey]);

  return (
    <main className="shell">
      <header className="topbar">
        <div className="brand"><span className="brand-mark">P</span><div><b>PHANTOM / SOL</b><small>CONTROL ROOM</small></div></div>
        <div className="mode"><i /> PAPER MODE <span>REAL TRADING DISABLED</span></div>
      </header>

      <section className="hero">
        <div><p className="eyebrow">SOLANA RESEARCH TERMINAL</p><h1>Market intelligence.<br /><em>Wallet visibility.</em></h1>
          <p className="sub">A read-only wallet dashboard connected to your paper-trading research engine.</p></div>
        <div className="hero-price"><small>BINANCE SPOT · SOLUSDC</small><strong>{price === null ? "—" : `${price.toFixed(4)}`}</strong><span>USDC / SOL · public ticker</span>{priceError && <small className="error">{priceError}</small>}</div>
      </section>

      <section className="grid">
        <article className="panel wallet-panel">
          <div className="panel-head"><div><small className="eyebrow">01 / WALLET</small><h2>Phantom connection</h2></div><span className="pill devnet">DEVNET ONLY</span></div>
          <p className="muted">Connect your Phantom wallet to inspect Devnet balances. This dashboard does not request signatures or send transactions.</p>
          <div className="connect-row"><ConnectButton fullWidth />{isConnected && <button className="ghost" onClick={() => void disconnect()} disabled={isDisconnecting}>{isDisconnecting ? "Disconnecting…" : "Disconnect"}</button>}</div>
          <div className="wallet-status"><span className={isConnected ? "dot green" : "dot"} />{isLoading ? "Initializing wallet SDK…" : isConnected ? "Wallet connected" : "Wallet not connected"}</div>
          {address && <div className="address"><small>PUBLIC SOLANA ADDRESS</small><b>{shortAddress(address)}</b><button onClick={() => navigator.clipboard.writeText(address)}>Copy</button></div>}
          <div className="balances">
            <div><small>SOL BALANCE · DEVNET</small><b>{balances ? balances.sol.toFixed(5) : "—"} <i>SOL</i></b></div>
            <div><small>USDC BALANCE · DEVNET</small><b>{balances ? balances.usdc.toFixed(2) : "—"} <i>USDC</i></b></div>
          </div>
          {balanceError && <p className="error">{balanceError}</p>}
          {isConnected && <button className="refresh" onClick={() => void refreshBalances()} disabled={refreshing}>{refreshing ? "Refreshing…" : "↻ Refresh balances"}</button>}
        </article>

        <article className="panel">
          <div className="panel-head"><div><small className="eyebrow">02 / SAFETY</small><h2>Execution controls</h2></div><span className="pill safe">LOCKED</span></div>
          <div className="control-list">
            <div><span>Paper trading</span><b className="green-text">ENABLED</b></div>
            <div><span>Wallet connection</span><b>OPTIONAL</b></div>
            <div><span>Transaction signing</span><b className="amber">NOT ENABLED</b></div>
            <div><span>Transaction broadcast</span><b className="red">BLOCKED</b></div>
            <div><span>Mainnet execution</span><b className="red">DISABLED</b></div>
          </div>
          <p className="footnote">No strategy signal can authorize a wallet action. No transaction builder, signer or broadcaster is exposed in this release.</p>
        </article>

        <article className="panel wide">
          <div className="panel-head"><div><small className="eyebrow">03 / MARKET DATA</small><h2>Exact market only</h2></div><span className="pill safe">PUBLIC DATA</span></div>
          <div className="market-row"><div><small>EXCHANGE</small><b>Binance Spot</b></div><div><small>SYMBOL</small><b>SOLUSDC</b></div><div><small>QUOTE</small><b>USDC</b></div><div><small>PRICE</small><b>{price === null ? "Unavailable" : price.toFixed(4)}</b></div></div>
          <p className="footnote">Ticker price is live public market data, not a closed-candle signal. The existing Python engine remains the source for closed-candle indicators and paper backtests.</p>
        </article>
      </section>
      <footer><span>PHANTOM CONNECT SDK · SOLANA DEVNET RPC</span><span>NO PRIVATE KEYS · NO REAL ORDERS · NO AUTO-SIGNING</span></footer>
    </main>
  );
}
