# Stock Chatbot — OpenAI Function Calling + yfinance

Chatbot de terminal em Python que entende pedidos em linguagem natural e, quando necessário, chama uma função Python para buscar o **preço de ações** em tempo real via `yfinance`. Suporta tickers internacionais e da B3 (ex.: `PETR4.SA`).

## 🚀 Recursos

* Conversa natural usando **OpenAI Chat Completions**
* **Function Calling** para buscar preço sob demanda
* Heurística para reconhecer tickers da B3 sem precisar digitar `.SA`
* Fácil de estender (ex.: variação %, horário da última cotação)

## 📁 Estrutura de Pastas

```
stock-chatbot-openai/
├─ README.md
├─ requirements.txt
├─ .gitignore
├─ .env.example
├─ main.py               # Loop principal do terminal
├─ chat.py               # Configuração do modelo e ciclo function calling
└─ finance_utils.py      # Funções utilitárias para buscar preços via yfinance
```

## 🛠️ Pré-requisitos

* Python 3.9+
* Conta na OpenAI (chave em `OPENAI_API_KEY`)

## 📦 Instalação

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

## ▶️ Uso

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

## 📄 .env.example

```dotenv
OPENAI_API_KEY=sua_chave_aqui
```

## 📜 Licença

Este projeto está licenciado sob os termos da licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## ⚠️ Observação

Este projeto é educativo e não constitui recomendação de investimento.
