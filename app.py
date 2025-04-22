from flask import Flask, jsonify, request
import firebase_admin
from firebase_admin import credentials, firestore
from flask_cors import CORS
import os
import json
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

# Pega a variável de ambiente e converte para JSON
FBKEY = json.loads(os.getenv('CONFIG_FIREBASE'))

cred = credentials.Certificate(FBKEY)
firebase_admin.initialize_app(cred)

# Conexão com o Firestore da Firebase
db = firestore.client()

# ROTA PRINCIPAL DE TESTE
@app.route('/')
def index():
    return 'API - CATRACA'

# GET - LISTAR ALUNOS
@app.route('/alunos/lista', methods=['GET'])
def alunos_lista():
    alunos = []
    lista = db.collection('alunos').stream()

    for item in lista:
        alunos.append(item.to_dict())
    
    if alunos:
        return jsonify(alunos), 200
    else:
        return jsonify({'mensagem':'Erro! Nenhum aluno encontrado.'}), 404

# GET - ALUNO POR ID
@app.route('/alunos/<id>', methods=['GET'])
def verificacao(id):
    doc_ref = db.collection('alunos').document(id)
    doc = doc_ref.get()

    if doc:
        return jsonify(doc.to_dict()), 200
    else:
        return jsonify({'mensagem': 'Erro! Esse ID não existe.'}), 404

# POST - CADASTRAR UM ALUNO
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    dados = request.json

    if "nome" not in dados or "cpf" not in dados:
        return jsonify({'mensagem': 'Erro! Todos os campos são obrigatórios.'}), 400
    
    # Define o status como True automaticamente
    status = True

    contador_ref = db.collection('controle_id').document('contador')
    contador_doc = contador_ref.get().to_dict()
    ultimo_id = contador_doc.get('id')
    novo_id = int(ultimo_id) + 1
    contador_ref.update({'id': novo_id})

    db.collection('alunos').document(str(novo_id)).set({
        "id": novo_id,
        "nome": dados['nome'],
        "cpf": dados['cpf'],
        "status": status
    })

    return jsonify({'mensagem': 'Aluno cadastrado com sucesso!'}), 201

# PUT - EDITAR ALUNO (nome, cpf e status)
@app.route('/alunos/<id>', methods=['PUT'])
def atualizar_aluno(id):
    doc_ref = db.collection('alunos').document(id)
    doc = doc_ref.get()

    if not doc:
        return jsonify({'mensagem': 'Aluno não encontrado.'}), 404

    dados = request.get_json()
    if not dados or not all(k in dados for k in ("nome", "cpf")):
        return jsonify({'mensagem': 'Erro! Campos nome e cpf são obrigatórios.'}), 400

    nome = dados['nome']
    cpf = dados['cpf']
    status = dados.get('status')

    if isinstance(status, str):
        status = status.lower() == 'true'

    update_data = {
        "nome": nome,
        "cpf": cpf,
        "status": status
    }

    doc_ref.update(update_data)
    return jsonify({'mensagem': 'Aluno atualizado com sucesso!'}), 200

# PATCH - ALTERAR APENAS O STATUS DO ALUNO
@app.route('/alunos/status/<id>', methods=['PATCH'])
def alterar_status(id):
    doc_ref = db.collection('alunos').document(id)
    doc = doc_ref.get()

    if not doc:
        return jsonify({'mensagem': 'Aluno não encontrado.'}), 404

    dados = request.get_json()
    if 'status' not in dados:
        return jsonify({'mensagem': 'Erro! O campo status é obrigatório.'}), 400

    status = dados['status']

    if isinstance(status, str):
        status = status.lower() == 'true'

    doc_ref.update({"status": status})

    return jsonify({'mensagem': 'Status atualizado com sucesso!'}), 200

# DELETE - EXCLUIR ALUNO
@app.route('/alunos/<id>', methods=['DELETE'])
def excluir_aluno(id):
    doc_ref = db.collection('alunos').document(id)
    doc = doc_ref.get()

    if not doc:
        return jsonify({'mensagem': 'ERRO! Aluno não encontrado!'}), 404

    doc_ref.delete()
    return jsonify({'mensagem': 'Aluno excluído com sucesso!'}), 201

if __name__ == '__main__':
    app.run()
