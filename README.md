# Stock Chatbot — OpenAI Function Calling + yfinance

Chatbot em **Python** que entende pedidos em linguagem natural e, quando necessário, chama uma função Python para buscar **preço de ações (tempo real e histórico)** via `yfinance`.  
Suporta tickers internacionais e da **B3** (ex.: `PETR4.SA`). Funciona no **terminal** e no **Telegram**.


## Recursos
- Conversa natural usando **OpenAI Chat Completions**
- **Function Calling** para buscar preços sob demanda
- Parâmetro **`period`** para consultas históricas (ex.: `"1y"`, `"6mo"`, `"1mo"`)
- Heurística para reconhecer tickers da B3 sem precisar digitar `.SA`
- Integração com **Telegram Bot** (modo polling)

## Estrutura de Pastas

```
stock-chatbot-openai/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ .env.example
├─ main.py               # Loop principal do terminal
├─ telegram_bot.py       # Bot telegram
├─ chat.py               # Configuração do modelo e ciclo function calling
└─ finance_utils.py      # Funções utilitárias para buscar preços via yfinance
```

## Pré-requisitos

* Python 3.9+
* Conta na OpenAI (chave em `OPENAI_API_KEY`)
* - (Opcional) Bot do Telegram criado no **@BotFather** (`TELEGRAM_BOT_TOKEN`)


## Instalação

```bash
# Criar ambiente virtual
python -m venv .venv
# Ativar ambiente (Windows)
.venv\Scripts\activate
# Ativar ambiente (Linux/Mac)
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Criar arquivo .env
cp .env.example .env
# Editar e colocar sua chave OPENAI_API_KEY no .env
```

## Uso

```bash
python main.py
```

Exemplos de entrada:

```
quanto está AAPL?
preço da PETR4
qual o preço de VALE3?
```

Para sair, digite `sair`.

## Uso no Telegram (opcional)

1. Crie um bot com **@BotFather** e pegue o token.
2. Coloque no `.env` a variável `TELEGRAM_BOT_TOKEN`.
3. Rode:
```bash
python telegram_bot.py

## .env.example

```dotenv
OPENAI_API_KEY=sua_chave_aqui
TELEGRAM_BOT_TOKEN=seu_token_telegram
```

## Observação

Este projeto é educativo e não constitui recomendação de investimento.
