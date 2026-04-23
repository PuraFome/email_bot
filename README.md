# # email_bot

## Descrição

O `email_bot` é uma aplicação Flask que envia emails para uma lista de destinatários e rastreia a abertura da mensagem usando um pixel de rastreamento. A aplicação está configurada para rodar em um contêiner Docker com um banco de dados PostgreSQL local.

## Funcionalidades

- Envio de emails para uma lista de destinatários.
- Rastreamento de abertura de emails usando um pixel de rastreamento.
- Registro de emails enviados e abertos em um banco de dados PostgreSQL local em Docker.

## Requisitos

- Python 3.9+
- Docker
- Node.js / npm

## Configuração

### Estrutura do projeto

- `backend/` — código Flask, conexões e lógica do serviço de email.
- `frontend/` — interface React com Vite.
- `docker-compose.yml` — orquestra PostgreSQL, backend e frontend.
- `postgres_data/` — pasta local onde o PostgreSQL salva dados.

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

```plaintext
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=email_bot
DB_HOST=postgres
DB_PORT=5432
SERVER_SMTP=smtp.gmail.com
PORTA_SMTP=587
SENDER_EMAIL=seu_email@gmail.com
PASSWORD=sua_senha_de_app
RANGE_DAYS=7
FLASK_ENV=development
FLASK_APP=app.py
```

### Executando com Docker

```bash
docker compose up --build
```

A aplicação backend ficará disponível em `http://localhost:5000` e o frontend em `http://localhost:3000`.
