import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from datetime import datetime
from decimal import Decimal

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()

# Inicializa a aplicação Flask e o SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- MODELOS DE DADOS ---

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # A relação "um-para-muitos". O backref cria um atributo '.category' no modelo Transaction.
    transactions = db.relationship('Transaction', backref='category', lazy=True)

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name
        }

class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    # db.Numeric(10, 2) é ideal para valores monetários (10 dígitos no total, 2 casas decimais)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    type = db.Column(db.String(7), nullable=False) # 'entrada' ou 'saída'
    # A Chave Estrangeira que cria a ligação com a tabela de categorias.
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def to_json(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': str(self.amount), # Convertemos para string para evitar problemas com JSON
            'date': self.date.isoformat(),
            'type': self.type,
            'category_id': self.category_id,
            'category_name': self.category.name if self.category else None
        }

# --- ROTAS DA API (Categorias) ---

# Rota para CRIAR uma nova categoria
@app.route('/api/categories', methods=['POST'])
def create_category():
    try:
        data = request.get_json()

        # Validação simples dos dados de entrada
        if not data or 'name' not in data or not data['name'].strip():
            return jsonify({'message': 'O nome da categoria é obrigatório.'}), 400

        category_name = data['name'].strip()

        # Verificar se a categoria já existe para evitar duplicados
        if Category.query.filter_by(name=category_name).first():
            return jsonify({'message': 'Essa categoria já existe.'}), 409 # 409 Conflict

        # Cria a nova categoria e salva no banco de dados
        new_category = Category(name=category_name)
        db.session.add(new_category)
        db.session.commit()

        return jsonify(new_category.to_json()), 201 # 201 Created
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar categoria', 'error': str(e)}), 500

# Rota para LISTAR todas as categorias
@app.route('/api/categories', methods=['GET'])
def get_categories():
    try:
        # Busca todas as categorias, ordenadas por nome
        categories = Category.query.order_by(Category.name).all()
        # Converte a lista de objetos para uma lista de JSON
        return jsonify([category.to_json() for category in categories]), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar categorias', 'error': str(e)}), 500


# Rota para CRIAR uma nova transação
@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    try:
        data = request.get_json()

        # Validação dos campos obrigatórios
        required_fields = ['description', 'amount', 'type', 'category_id']
        if not all(field in data for field in required_fields):
            return jsonify({'message': 'Campos em falta'}), 400

        # Validação do tipo de transação
        if data['type'] not in ['entrada', 'saída']:
            return jsonify({'message': 'O tipo deve ser "entrada" ou "saída"'}), 400

        # Validação e conversão do valor
        try:
            amount = Decimal(data['amount'])
            if amount <= 0:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({'message': 'O valor (amount) deve ser um número positivo'}), 400

        # Validação da data
        try:
            # Se a data for enviada, usa-a. Se não, usa a data atual.
            transaction_date = datetime.fromisoformat(data['date']) if 'date' in data else datetime.utcnow()
        except ValueError:
            return jsonify({'message': 'Formato de data inválido. Use AAAA-MM-DD'}), 400


        # Validação da categoria: verificar se a categoria existe
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'message': 'Categoria não encontrada'}), 404 # 404 Not Found

        # Cria a nova transação
        new_transaction = Transaction(
            description=data['description'],
            amount=amount,
            type=data['type'],
            date=transaction_date,
            category_id=data['category_id']
        )

        db.session.add(new_transaction)
        db.session.commit()

        return jsonify(new_transaction.to_json()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao criar transação', 'error': str(e)}), 500

# Rota para LISTAR todas as transações
@app.route('/api/transactions', methods=['GET'])
def get_transactions():
    try:
        # Busca todas as transações, ordenadas por data descendente (mais recentes primeiro)
        transactions = Transaction.query.order_by(Transaction.date.desc()).all()
        return jsonify([transaction.to_json() for transaction in transactions]), 200
    except Exception as e:
        return jsonify({'message': 'Erro ao buscar transações', 'error': str(e)}), 500

# --- PONTO DE ENTRADA ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
