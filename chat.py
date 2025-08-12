import json
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Definição da ferramenta que o modelo pode chamar
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": (
                "Obtém preço de ação. Se 'period' for maior que 1 dia (ex.: '1y', '6mo'), "
                "retorna também preço inicial e variação percentual no período."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "Símbolo da ação. Ex.: AAPL, MSFT, PETR4.SA"
                    },
                    "period": {
                        "type": "string",
                        "description": "Janela histórica do yfinance (ex.: '1d', '5d', '1mo', '6mo', '1y', '5y', 'max'). Padrão: '1d'."
                    }
                },
                "required": ["ticker"]
            }
        }
    }
]

SYSTEM_PROMPT = (
    "Você é um assistente financeiro de terminal. "
    "Quando o usuário pedir preço atual, chame get_stock_price sem 'period' ou com '1d'. "
    "Quando pedir variação/valor histórico (ex.: 'último ano', '6 meses', 'mês passado'), "
    "passe um 'period' apropriado do yfinance (ex.: '1y', '6mo', '1mo'). "
    "Explique de forma curta e clara."
    "Formate SEMPRE a resposta em HTML adequada ao Telegram (parse_mode=HTML), no seguinte estilo:\n"
    "<b>{TICKER}</b> — {NOME_OPCIONAL}\n"
    "Preço: <b>{PRICE} {CUR}</b>\n"
    "{SE_PERIOD>1D: Início: {PRICE_START} · Variação: <b>{VAR}%</b>}\n"
    "Obs.: Seja sucinto e não use tags fora de <b> e <i>."
)



def run_round(user_message: str, get_price_fn, model: str = "gpt-4o-mini") -> str:
    """Executa uma rodada de conversa: modelo decide se chama a função; se sim, roda e retorna resposta final."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    # 1) Primeira chamada — o modelo pode pedir a função
    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
        temperature=0
    )
    msg = resp.choices[0].message

    # 2) Se houver function calling, execute e devolva
    if msg.tool_calls:
        messages.append({
            "role": "assistant",
            "content": None,
            "tool_calls": msg.tool_calls
        })

        for tc in msg.tool_calls:
            if tc.type == "function" and tc.function.name == "get_stock_price":
                args = json.loads(tc.function.arguments or "{}")
                result = get_price_fn(**args)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "name": tc.function.name,
                    "content": json.dumps(result, ensure_ascii=False)
                })

        # 3) Segunda chamada — resposta final usando o resultado
        final = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0
        )
        return final.choices[0].message.content or ""

    # Caso não precise de ferramenta
    return msg.content or ""

