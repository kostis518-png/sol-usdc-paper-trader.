#!/usr/bin/env python3
"""Paper-only Binance Spot SOL/USDC research runner. Public market data only."""
import argparse, json, os, time, urllib.parse, urllib.request
from datetime import datetime, timezone

BASE="https://api.binance.com"
SYMBOL="SOLUSDC"
INTERVAL="15m"
STEP=15*60*1000
FEE=0.001
SLIPPAGE=0.0005
RISK=0.005
STOP_ATR=1.5
TARGET_R=2.0

def api(path, params=None):
    query=urllib.parse.urlencode(params or {})
    req=urllib.request.Request(BASE+path+("?"+query if query else ""),headers={"User-Agent":"sol-usdc-paper-trader/1.0"})
    with urllib.request.urlopen(req,timeout=20) as response:
        return json.loads(response.read().decode("utf-8"))

def candles(days):
    info=api("/api/v3/exchangeInfo",{"symbol":SYMBOL})
    market=info.get("symbols",[])
    if not market or market[0].get("status")!="TRADING" or market[0].get("baseAsset")!="SOL" or market[0].get("quoteAsset")!="USDC":
        raise RuntimeError("Exact Binance Spot SOL/USDC market unavailable; refusing substitutions.")
    now=int(info["serverTime"]); start=now-days*86400000; rows=[]
    while start<now:
        batch=api("/api/v3/klines",{"symbol":SYMBOL,"interval":INTERVAL,"startTime":start,"endTime":now,"limit":1000})
        if not batch: break
        rows.extend(batch); nxt=int(batch[-1][0])+STEP
        if nxt<=start: raise RuntimeError("Kline pagination did not advance.")
        start=nxt
        if len(batch)<1000: break
        time.sleep(0.15)
    unique={int(r[0]):r for r in rows if int(r[6])<now}
    out=[]
    for r in sorted(unique.values(),key=lambda x:int(x[0])):
        out.append({"open_time":int(r[0]),"open":float(r[1]),"high":float(r[2]),"low":float(r[3]),"close":float(r[4]),"volume":float(r[5]),"close_time":int(r[6])})
    if len(out)<60: raise RuntimeError("Insufficient closed candles.")
    return out,now

def ema(values,n):
    out=[None]*len(values)
    if len(values)<n:return out
    v=sum(values[:n])/n;out[n-1]=v;a=2/(n+1)
    for i in range(n,len(values)):
        v=values[i]*a+v*(1-a);out[i]=v
    return out

def indicators(cs):
    close=[c["close"] for c in cs];e20=ema(close,20);e50=ema(close,50)
    gain=[0.0];loss=[0.0];tr=[cs[0]["high"]-cs[0]["low"]]
    for i in range(1,len(cs)):
        d=close[i]-close[i-1];gain.append(max(d,0));loss.append(max(-d,0))
        tr.append(max(cs[i]["high"]-cs[i]["low"],abs(cs[i]["high"]-close[i-1]),abs(cs[i]["low"]-close[i-1])))
    rsi=[None]*len(cs);atr=[None]*len(cs)
    if len(cs)>14:
        ag=sum(gain[1:15])/14;al=sum(loss[1:15])/14;av=sum(tr[1:15])/14
        for i in range(14,len(cs)):
            if i>14:ag=(ag*13+gain[i])/14;al=(al*13+loss[i])/14;av=(av*13+tr[i])/14
            rsi[i]=100 if al==0 else 100-100/(1+ag/al);atr[i]=av
    for i,c in enumerate(cs):c.update(ema20=e20[i],ema50=e50[i],rsi14=rsi[i],atr14=atr[i])
    return cs

def enter(c):
    return c["ema20"] is not None and c["ema50"] is not None and c["rsi14"] is not None and c["atr14"] is not None and c["ema20"]>c["ema50"] and 52<=c["rsi14"]<=68 and c["close"]>c["ema20"]

def leave(c):
    return c["ema20"] is not None and c["ema50"] is not None and c["rsi14"] is not None and (c["ema20"]<c["ema50"] or c["rsi14"]<45)

def backtest(cs):
    cash=1000.0;peak=cash;maxdd=0.0;pos=None;trades=[]
    for i in range(51,len(cs)-1):
        c,nxt=cs[i],cs[i+1]
        if pos:
            reason=raw=None
            if c["low"]<=pos["stop"]:reason,raw="stop",pos["stop"]
            elif c["high"]>=pos["target"]:reason,raw="take_profit",pos["target"]
            elif leave(c):reason,raw="indicator_exit",c["close"]
            if reason:
                fill=raw*(1-SLIPPAGE);proceeds=pos["qty"]*fill*(1-FEE);pnl=proceeds-pos["cost"];cash+=proceeds
                trades.append({"pnl":pnl,"reason":reason});pos=None
        if pos is None and enter(c):
            entry=nxt["open"]*(1+SLIPPAGE);stop=entry-STOP_ATR*c["atr14"];risk_unit=entry-stop
            qty=min(cash*RISK/risk_unit,cash/(entry*(1+FEE))) if risk_unit>0 else 0
            cost=qty*entry*(1+FEE)
            if qty>0 and cost<=cash:
                cash-=cost;pos={"qty":qty,"entry":entry,"stop":stop,"target":entry+TARGET_R*risk_unit,"cost":cost}
        marked=cash+(pos["qty"]*c["close"] if pos else 0);peak=max(peak,marked);maxdd=max(maxdd,(peak-marked)/peak if peak else 0)
    wins=sum(t["pnl"]>0 for t in trades)
    return {"trades":len(trades),"pnl":sum(t["pnl"] for t in trades),"cash":cash,"win_rate":100*wins/len(trades) if trades else None,"max_dd":100*maxdd}

def main():
    p=argparse.ArgumentParser();p.add_argument("--days",type=int,default=30);p.add_argument("--output",default="reports/latest.md");a=p.parse_args()
    cs,server=candles(a.days);indicators(cs);last=cs[-1];bt=backtest(cs)
    ticker=float(api("/api/v3/ticker/price",{"symbol":SYMBOL})["price"])
    closed=datetime.fromtimestamp(last["close_time"]/1000,timezone.utc).isoformat()
    fetched=datetime.fromtimestamp(server/1000,timezone.utc).isoformat()
    signal="PAPER LONG SETUP" if enter(last) else "NO ENTRY"
    reasons=[]
    if last["ema20"]<=last["ema50"]:reasons.append("EMA20 is not above EMA50")
    if not 52<=last["rsi14"]<=68:reasons.append("RSI14 is outside 52-68")
    if last["close"]<=last["ema20"]:reasons.append("close is not above EMA20")
    lines=["# SOL/USDC Paper-Trading Report","",f"- Exact Binance Spot market: {SYMBOL} (verified TRADING)",
      f"- Data fetched: {fetched}","- Interval: 15m; closed candles only",f"- Latest closed candle: {closed}",
      f"- Latest closed close: {last['close']:.4f} USDC",f"- Current spot ticker (not candle close): {ticker:.4f} USDC","",
      "## Indicators","", "| EMA20 | EMA50 | RSI14 | ATR14 |","|---:|---:|---:|---:|",
      f"| {last['ema20']:.4f} | {last['ema50']:.4f} | {last['rsi14']:.2f} | {last['atr14']:.4f} |","",
      "## Signal","",f"**{signal}**"]
    if reasons:lines.append("Reason: "+"; ".join(reasons)+".")
    if enter(last):
        stop=last["close"]-STOP_ATR*last["atr14"];target=last["close"]+TARGET_R*(last["close"]-stop)
        lines += [f"- Reference close entry: {last['close']:.4f}",f"- Illustrative ATR stop: {stop:.4f}",f"- Illustrative 2R target: {target:.4f}","- Simulated execution would occur at next candle open."]
    lines += ["","## 30-day rolling backtest","",f"- Closed trades: {bt['trades']}",f"- Realized net P&L: {bt['pnl']:.2f} USDC (1,000 USDC initial equity)",f"- Win rate: {'n/a' if bt['win_rate'] is None else f'{bt["win_rate"]:.2f}%'}",f"- Maximum marked-to-market drawdown: {bt['max_dd']:.2f}%",
      f"- Assumed fee: {FEE*100:.2f}% each side; slippage: {SLIPPAGE*100:.2f}% each side",f"- Risk budget: {RISK*100:.2f}% equity; stop: {STOP_ATR}x ATR; target: {TARGET_R}R",
      "","## Rules and limitations","",
      "- Long-only spot; one open position maximum; no leverage or shorting.",
      "- Entry: EMA20 > EMA50, RSI14 52-68, close > EMA20. Exit: stop, 2R target, EMA20 < EMA50, or RSI14 < 45.",
      "- Backtest enters at next candle open; stop is assumed first if stop and target touch in the same candle.",
      "- Fees and slippage are estimates, not account-specific actuals.",
      "- Research baseline only; not yet validated as profitable. No API keys, wallet access, or order placement.",""]
    report="\n".join(lines);os.makedirs(os.path.dirname(a.output) or ".",exist_ok=True)
    with open(a.output,"w",encoding="utf-8") as f:f.write(report)
    print(report)

if __name__=="__main__":main()
