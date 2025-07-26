# API de Rastreador de Finanças Pessoais (Projeto 2 - Nova Série)

Este projeto consiste numa API RESTful robusta para a gestão de finanças pessoais, construída com **Python**, **Flask** e **PostgreSQL**. É uma aplicação que vai além de um simples CRUD, implementando um modelo de dados relacional, validações de dados e funcionalidades de consulta avançadas, como filtros e busca de texto.

---

## ✨ Funcionalidades e Conceitos Aplicados

* **CRUD Completo para Categorias e Transações:** Implementação de todas as operações (Create, Read, Update, Delete) para os dois principais recursos da API.
* **Modelo de Dados Relacional:** Utilização de uma relação "Um-para-Muitos" entre Categorias e Transações, garantindo a integridade dos dados através de chaves estrangeiras (`ForeignKey`).
* **Validação de Dados no Backend:** A API valida os dados de entrada para garantir a sua consistência, verificando campos obrigatórios, tipos de dados (ex: "entrada" vs "saída") e a existência de recursos relacionados (ex: uma transação só pode ser associada a uma categoria que exista).
* **Querying Avançado:** O endpoint de listagem de transações (`GET /api/transactions`) foi enriquecido com superpoderes:
    * **Filtragem por Data:** Permite filtrar transações por ano e/ou mês.
    * **Filtragem por Categoria:** Permite ver apenas as transações de uma categoria específica.
    * **Busca por Texto:** Implementa uma funcionalidade de "search bar" que faz uma busca *case-insensitive* no campo de descrição.
* **SQLAlchemy ORM:** Todo o acesso à base de dados é gerido pelo SQLAlchemy, que traduz classes Python para tabelas SQL e permite a construção de queries complexas de forma programática.

---

## 🛠️ Tech Stack & Ferramentas

* **Linguagem:** Python
* **Framework:** Flask
* **Banco de Dados:** PostgreSQL
* **ORM:** SQLAlchemy (com a extensão Flask-SQLAlchemy)
* **Driver do Banco de Dados:** `psycopg2-binary`
* **Gerenciamento de Ambiente:** `venv` e `pip`
* **Gestão de Segredos:** `python-dotenv`

---

## 📖 Documentação da API (Endpoints)

### Recursos de Categorias (`/api/categories`)

| Método | Endpoint         | Descrição                  | Corpo (Body) da Requisição    | Resposta de Sucesso |
| :----- | :--------------- | :------------------------- | :--------------------------- | :------------------ |
| `POST` | `/api/categories`  | Cria uma nova categoria.   | `{ "name": "Alimentação" }`  | `201 Created`       |
| `GET`  | `/api/categories`  | Lista todas as categorias. | *Nenhum* | `200 OK`            |

### Recursos de Transações (`/api/transactions`)

| Método   | Endpoint               | Descrição                                                                      | Corpo (Body) da Requisição                                                                   | Resposta de Sucesso |
| :------- | :--------------------- | :----------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- | :------------------ |
| `POST`   | `/api/transactions`      | Cria uma nova transação.                                                       | `{ "description": "...", "amount": "15.50", "type": "saída", "category_id": 1, "date": "YYYY-MM-DD" }` | `201 Created`       |
| `GET`    | `/api/transactions`      | Lista todas as transações, com filtros opcionais.                              | *Nenhum* | `200 OK`            |
| `PUT`    | `/api/transactions/<id>` | Atualiza uma transação existente.                                              | `{ "description": "...", "amount": "20.00" }` (campos opcionais)                             | `200 OK`            |
| `DELETE` | `/api/transactions/<id>` | Deleta uma transação.                                                          | *Nenhum* | `200 OK`            |

**Parâmetros de Consulta para `GET /api/transactions`:**
Os filtros podem ser combinados na URL.
* `?year=<ano>` (ex: `?year=2025`)
* `?month=<mês>` (ex: `?month=7`)
* `?category_id=<id>` (ex: `?category_id=1`)
* `?search=<termo>` (ex: `?search=café`)

---

## ⚙️ Como Executar o Projeto Localmente

**Pré-requisitos:**
* Python 3
* Servidor PostgreSQL instalado e a correr
* Git

**Passos:**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/api-finance-tracker.git](https://github.com/seu-usuario/api-finance-tracker.git)
    cd api-finance-tracker
    ```

2.  **Crie e Ative o Ambiente Virtual (`venv`).**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure o Banco de Dados:**
    * No terminal `psql`, crie a base de dados: `CREATE DATABASE finance_tracker_db;`

5.  **Configure as Variáveis de Ambiente:**
    * Crie um ficheiro `.env` na raiz do projeto e adicione a sua `DATABASE_URL`. Exemplo:
        `DATABASE_URL=postgresql://user:password@localhost:5432/finance_tracker_db`

6.  **Crie as Tabelas da Aplicação:**
    * No terminal (com o `venv` ativo), execute: `flask shell`
    * Dentro do shell, execute:
        ```python
        >>> from app import db
        >>> db.create_all()
        >>> exit()
        ```

7.  **Execute o servidor:**
    ```bash
    python3 app.py
    ```
    O servidor estará a correr em `http://localhost:5000`.