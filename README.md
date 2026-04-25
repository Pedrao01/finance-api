# 💰 Finance API

Uma API REST para gerenciamento de transações financeiras, construída com **Django** e **Django REST Framework**, com autenticação via **JWT** e banco de dados **PostgreSQL**.

---

## 🚀 Tecnologias

- [Python 3.x](https://www.python.org/)
- [Django 5.2](https://www.djangoproject.com/)
- [Django REST Framework 3.17](https://www.django-rest-framework.org/)
- [Simple JWT 5.5](https://django-rest-framework-simplejwt.readthedocs.io/)
- [PostgreSQL 16](https://www.postgresql.org/)
- [Docker & Docker Compose](https://www.docker.com/)
- [python-decouple](https://github.com/HBNetwork/python-decouple) — gerenciamento de variáveis de ambiente

---

## 📁 Estrutura do Projeto

```
finance-api/
├── config/
│   ├── settings/
│   │   ├── base.py          # Configurações base
│   │   ├── development.py   # Configurações de desenvolvimento
│   │   └── production.py    # Configurações de produção
│   ├── urls.py              # Roteamento principal
│   ├── asgi.py
│   └── wsgi.py
├── users/
│   ├── migrations/          # Migrações do banco de dados
│   ├── models.py            # Modelos: User e Transaction
│   ├── serializers.py       # Serializers DRF
│   ├── services.py          # Regras de negócio
│   └── views.py             # Views da API
├── docker-compose.yml
├── manage.py
└── requirements.txt
```

---

## ⚙️ Configuração do Ambiente

### Pré-requisitos

- Python 3.10+
- Docker e Docker Compose
- pip

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/finance-api.git
cd finance-api
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv .venv

# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto com base no exemplo abaixo:

```env
SECRET_KEY=sua-secret-key-aqui

DB_NAME=finance_db
DB_USER=postgres
DB_PASSWORD=sua-senha
DB_HOST=localhost
DB_PORT=5433
```

### 5. Suba o banco de dados com Docker

```bash
docker-compose up -d
```

### 6. Execute as migrações

```bash
python manage.py migrate
```

### 7. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

A API estará disponível em `http://localhost:8000`.

---

## 🔑 Autenticação

A API utiliza autenticação **JWT (JSON Web Token)**. Para acessar os endpoints protegidos, inclua o token no cabeçalho da requisição:

```
Authorization: Bearer <seu_token>
```

---

## 📡 Endpoints

### Usuários

| Método | Endpoint      | Autenticação | Descrição              |
|--------|---------------|-------------|------------------------|
| POST   | `/api/users/` | Não         | Cadastrar novo usuário |

**Body (JSON):**
```json
{
  "username": "joao",
  "email": "joao@email.com",
  "password": "senha1234",
  "cpf": "12345678901",
  "phone_number": "11999999999"
}
```

**Resposta (201):**
```json
{
  "id": 1,
  "email": "joao@email.com"
}
```

---

### Autenticação

| Método | Endpoint             | Descrição                        |
|--------|----------------------|----------------------------------|
| POST   | `/api/auth/login/`   | Obter par de tokens (access + refresh) |
| POST   | `/api/auth/refresh/` | Renovar o access token           |

**Body (login):**
```json
{
  "username": "joao",
  "password": "senha1234"
}
```

---

### Transações

> Todos os endpoints de transações exigem autenticação JWT.

| Método | Endpoint             | Descrição                              |
|--------|----------------------|----------------------------------------|
| GET    | `/api/transactions/` | Listar transações do usuário autenticado (paginado) |
| POST   | `/api/transactions/` | Criar nova transação                   |

**Body (POST):**
```json
{
  "value": "150.00",
  "kind": "credit"
}
```

> `kind` aceita: `"credit"` ou `"debit"`

**Resposta (201):**
```json
{
  "id": 1,
  "value": "150.00",
  "kind": "credit",
  "status": "pending",
  "created_at": "2026-04-25T15:00:00Z",
  "user": { ... }
}
```

**Status possíveis de uma transação:** `pending` · `completed` · `cancelled`

---

## 📐 Regras de Negócio

- O usuário deve estar **ativo** para criar transações.
- O campo `kind` deve ser `credit` ou `debit` — valores inválidos retornam erro 400.
- Transações são criadas atomicamente via `transaction.atomic()`.
- CPF é único por usuário.
- A listagem de transações retorna apenas as do **usuário autenticado**, com paginação (`limit`/`offset`, padrão 5 por página).

---

## 🛡️ Rate Limiting

Configurado por padrão no DRF:

| Tipo          | Limite      |
|---------------|-------------|
| Anônimo       | 100/dia     |
| Autenticado   | 1000/dia    |

---

## 🗄️ Modelos

### `User`
Estende `AbstractUser` com os campos adicionais:
- `cpf` — CharField único, máx. 11 caracteres
- `phone_number` — CharField opcional, máx. 13 caracteres

### `Transaction`
- `user` — ForeignKey para `User`
- `value` — DecimalField (máx. 11 dígitos, 2 casas decimais)
- `kind` — `credit` ou `debit`
- `status` — `pending`, `completed` ou `cancelled`
- `created_at` — DateTimeField (auto)

---

## 🐳 Docker

O `docker-compose.yml` sobe apenas o serviço de banco de dados PostgreSQL:

```bash
# Subir o banco
docker-compose up -d

# Parar
docker-compose down
```

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.
