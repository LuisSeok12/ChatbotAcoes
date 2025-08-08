import yfinance as yf

def _maybe_b3_suffix(ticker: str) -> str:
    t = ticker.strip().upper()
    # Heurística: tickers da B3 costumam terminar com número (ex.: PETR4). Se não houver sufixo, adiciona .SA
    if "." not in t and any(ch.isdigit() for ch in t[-2:]):
        t += ".SA"
    return t


def get_stock_price(ticker: str) -> dict:
    """Retorna {ok, ticker, price, currency} ou {ok: False, error} usando yfinance."""
    t = _maybe_b3_suffix(ticker)
    acao = yf.Ticker(t)

    # Tenta via fast_info (mais rápido)
    price = None
    currency = None
    try:
        fi = getattr(acao, "fast_info", None)
        if fi and getattr(fi, "last_price", None):
            price = float(fi.last_price)
            currency = getattr(fi, "currency", None)
    except Exception:
        pass

    # Fallback para history
    if price is None:
        dados = acao.history(period="1d")
        if dados.empty:
            return {"ok": False, "error": f"Sem dados para {ticker}."}
        price = float(dados["Close"].iloc[-1])

    # Descobre moeda se ainda não tiver
    if not currency:
        try:
            info = acao.get_info()
            currency = info.get("currency")
        except Exception:
            currency = None

    return {
        "ok": True,
        "ticker": t,
        "price": price,
        "currency": currency or "?"
    }