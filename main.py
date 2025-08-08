import os
from dotenv import load_dotenv
from chat import run_round
from finance_utils import get_stock_price

load_dotenv()

BANNER = (
    "=== Stock Chatbot ===\n"
    "Digite um pedido, ex.: 'quanto está AAPL?', 'preço da PETR4', 'e a VALE3?'.\n"
    "Escreva 'sair' para encerrar.\n"
)


def main():
    print(BANNER)
    while True:
        user = input("> ").strip()
        if not user:
            continue
        if user.lower() in {"sair", "exit", "quit"}:
            print("Até mais!")
            break
        try:
            answer = run_round(user, get_stock_price)
            print(answer)
        except Exception as e:
            print(f"[erro] {e}")


if __name__ == "__main__":
    main()