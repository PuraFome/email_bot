# # email_bot

## Descrição

O `email_bot` é uma aplicação Flask que envia emails para uma lista de destinatários e rastreia a abertura dos emails usando um pixel de rastreamento. A aplicação está configurada para rodar em um contêiner Docker e pode ser implantada no Google Cloud Run.

## Funcionalidades

- Envio de emails para uma lista de destinatários.
- Rastreamento de abertura de emails usando um pixel de rastreamento.
- Registro de emails enviados e abertos em um banco de dados CockroachDB.

## Requisitos

- Python 3.9+
- Docker
- Google Cloud SDK
- Conta no Google Cloud
- um banco de dados online qualquer (ex: CockroachDB)

## Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis de ambiente:

```plaintext
DATABASE_URL=postgresql://<usuario>:<senha>@<host>:<porta>/<database>?sslmode=verify-full
SERVER_SMTP=smtp.gmail.com
PORTA_SMTP=587
SENDER_EMAIL=seu_email@gmail.com
PASSWORD=sua_senha
RANGE_DAYS=7 (dias entre os envios)
```