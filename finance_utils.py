import yfinance as yf
from datetime import datetime

def _maybe_b3_suffix(ticker: str) -> str:
    t = ticker.strip().upper()
    if "." not in t and any(ch.isdigit() for ch in t[-2:]):
        t += ".SA"
    return t

def get_stock_price(ticker: str, period: str = "1d") -> dict:
    """
    Retorna:
      - sempre: {ok, ticker, currency, price, timestamp}
      - se period == '1d': também {open, high, low}
      - se period != '1d': também {price_start, variation_percent}
    """
    t = _maybe_b3_suffix(ticker)
    acao = yf.Ticker(t)

    dados = acao.history(period=period)
    if dados.empty:
        return {"ok": False, "error": f"Sem dados para {ticker} no período {period}."}

    last = dados.iloc[-1]
    price = float(last["Close"])

    # timestamp do último candle
    ts = last.name
    if isinstance(ts, datetime):
        timestamp = ts.strftime("%Y-%m-%d %H:%M")
    else:
        timestamp = str(ts)

    # evita get_info(): assume BRL para .SA; senão, deixa "USD" como default simples
    currency = "BRL" if t.endswith(".SA") else "USD"

    resp = {
        "ok": True,
        "ticker": t,
        "currency": currency,
        "price": round(price, 2),
        "timestamp": timestamp,
    }

    if period == "1d":
        resp.update({
            "open": round(float(last["Open"]), 2),
            "high": round(float(last["High"]), 2),
            "low":  round(float(last["Low"]), 2),
        })
    else:
        first = dados.iloc[0]
        price_start = float(first["Close"])
        var_pct = ((price - price_start) / price_start) * 100
        resp.update({
            "price_start": round(price_start, 2),
            "variation_percent": round(var_pct, 2),
        })

    return resp


