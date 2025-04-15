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

#GET - LISTAR ALUNOS
@app.route('/alunos/lista', methods=['GET'])
def alunos_lista():
    alunos = []
    lista = db.collection('alunos').stream()

    for item in lista:
        alunos.append(item.to_dict())
    
    if alunos:
        return jsonify(alunos), 200
    else:
        return jsonify({'mensagem':'Erro! Nenhuma aluno encontrado.'}), 404

#GET - ALUNO POR ID
@app.route('/alunos/<id>', methods=['GET'])
def verificacao(id):
    doc_ref = db.collection('alunos').document(id)
    doc = doc_ref.get().to_dict()

    if doc:
        return jsonify(doc), 200
    else:
        return jsonify({'mensagem': 'Erro! Esse ID não existe.'}), 404

#POST - CADASTRAR UM ALUNO
@app.route('/alunos', methods=['POST'])
def cadastrar_aluno():
    dados = request.json

    if "nome" not in dados or "cpf" not in dados or "status" not in dados:
        return jsonify({'mensagem': 'Erro! Todos os campos são obrigatórios.'}), 400
    
    status = dados['status']
    if isinstance(status, str):
        status = status.lower() == 'true'

    contador_ref = db.collection('controle_id').document('contador')
    contador_doc = contador_ref.get().to_dict()
    ultimo_id = contador_doc.get('id')
    novo_id = int(ultimo_id) + 1
    contador_ref.update({'id': novo_id})

    db.collection('alunos').document(str(novo_id)).set({
        "id":novo_id,
        "nome": dados['nome'],
        "cpf": dados['cpf'],
        "status": status
    })

    return jsonify({'mensagem': 'Aluno cadastrado com sucesso!'}), 201


#PUT - EDITAR ALUNO
@app.route('/alunos/<id>', methods=['PUT'])
def editar_aluno(id):
    dados = request.json

    if "nome" not in dados or "cpf" not in dados or "status" not in dados:
        return jsonify({'mensagem': 'Erro! Todos os campos são obrigatórios.'}), 400

    doc_ref = db.collection('alunos').document(id)
    doc = doc_ref.get()

    if doc:
        doc_ref.update({
            "nome": dados['nome'],
            "cpf": dados['cpf'],
            "status": dados['status']
        })
        return jsonify({'mensagem': 'Aluno atualizado com sucesso!'}), 201
    else:
        return jsonify({'mensagem': 'ERRO! ID não encontrado.'}), 404

#DELETE - EXCLUIR ALUNO
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