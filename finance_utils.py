import yfinance as yf

def _maybe_b3_suffix(ticker: str) -> str:
    t = ticker.strip().upper()
    # Heurística: tickers da B3 costumam terminar com número (ex.: PETR4). Se não houver sufixo, adiciona .SA
    if "." not in t and any(ch.isdigit() for ch in t[-2:]):
        t += ".SA"
    return t


def get_stock_price(ticker: str, period: str = "1d") -> dict:
    """
    Retorna {ok, ticker, price, currency} ou {ok: False, error} usando yfinance.
    Se period != '1d', retorna também preço inicial e variação percentual no período.
    """
    t = _maybe_b3_suffix(ticker)
    acao = yf.Ticker(t)

    # Busca histórico do período desejado
    dados = acao.history(period=period)
    if dados.empty:
        return {"ok": False, "error": f"Sem dados para {ticker} no período {period}."}

    preco_atual = float(dados["Close"].iloc[-1])
    moeda = acao.info.get("currency", "?")

    retorno = {
        "ok": True,
        "ticker": t,
        "currency": moeda,
        "price": preco_atual
    }

    # Se for mais de 1 dia, calcula preço inicial e variação
    if period != "1d":
        preco_inicial = float(dados["Close"].iloc[0])
        variacao = ((preco_atual - preco_inicial) / preco_inicial) * 100
        retorno.update({
            "price_start": preco_inicial,
            "variation_percent": round(variacao, 2)
        })

    return retorno
