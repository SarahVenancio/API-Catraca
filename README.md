
# 🎓 API Catraca - Controle de Acesso de Alunos

A **API Catraca** é uma aplicação backend desenvolvida em Python com o microframework **Flask** que simula um sistema de controle de entrada e saída de alunos, como uma catraca digital. Utiliza o **Firebase Firestore** como banco de dados para armazenar os registros dos alunos, oferecendo um CRUD completo e seguro via HTTP REST API.

---

## 📌 Detalhamento do Projeto

O objetivo desta API é fornecer um sistema simples e funcional para o gerenciamento de alunos em instituições de ensino. Ela pode ser integrada a sistemas de catraca física ou controle interno, fornecendo funcionalidades como:

- Cadastro de novos alunos
- Consulta de alunos existentes
- Atualização de dados e status de acesso
- Exclusão de registros
- Integração com Firebase Firestore, facilitando o deploy em nuvem

A estrutura do banco de dados segue uma lógica simples baseada em documentos e coleções, sendo ideal para aplicações web, móveis ou embarcadas.

---

## ✨ Funcionalidades

- ✅ **Listar alunos** – Retorna todos os alunos cadastrados
- ✅ **Buscar por ID** – Retorna os dados de um aluno específico
- ✅ **Cadastrar aluno** – Insere novo aluno com nome, CPF e status ativo
- ✅ **Atualizar aluno** – Edita os dados de nome, CPF e status
- ✅ **Alterar status** – Atualiza apenas o status do aluno (ativo/inativo)
- ✅ **Excluir aluno** – Remove permanentemente o registro

---

## 🧱 Estrutura do Firestore

```
alunos (collection)
  └── <id> (document)
      ├── nome: string
      ├── cpf: string
      └── status: boolean

controle_id (collection)
  └── contador (document)
      └── id: number
```

---

## 📦 Instalação e Configuração

### ✅ Pré-requisitos

- Python 3.8 ou superior
- Conta no Firebase com o Firestore ativado
- Credencial do Firebase (Service Account) no formato JSON

### 🔨 Etapas

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/api-catraca.git
   cd api-catraca
   ```

2. **Crie um ambiente virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Crie um arquivo `.env` com sua chave do Firebase:**
   ```env
   CONFIG_FIREBASE={"type": "service_account", "project_id": "...", ...}
   ```

5. **Configure o Firestore:**
   - Crie a coleção `alunos`
   - Crie a coleção `controle_id` com o documento `contador`:
     ```json
     {
       "id": 0
     }
     ```

6. **Inicie o servidor:**
   ```bash
   python app.py
   ```

---

## 🔍 Endpoints da API

### Teste de conexão
```http
GET /
```

### Listar todos os alunos
```http
GET /alunos/lista
```

### Buscar aluno por ID
```http
GET /alunos/<id>
```

### Cadastrar novo aluno
```http
POST /alunos
Content-Type: application/json

{
  "nome": "João Silva",
  "cpf": "12345678900"
}
```

### Atualizar dados do aluno
```http
PUT /alunos/<id>
Content-Type: application/json

{
  "nome": "João Atualizado",
  "cpf": "99999999999",
  "status": true
}
```

### Atualizar apenas o status
```http
PATCH /alunos/status/<id>
Content-Type: application/json

{
  "status": false
}
```

### Excluir aluno
```http
DELETE /alunos/<id>
```

## Links para acessar o projeto na Vercel:
- [API](https://api-catraca-weld.vercel.app/)
- [Catraca](https://academiamoveup.vercel.app/)
- [ADM](https://moveupadmin.vercel.app/)

## Autores
| [<img src="https://avatars.githubusercontent.com/u/165316263?v=4" width=115><br><sub>Sarah Dias Venâncio</sub>](https://github.com/SarahVenancio) |  [<img src="https://avatars.githubusercontent.com/u/165318420?s=100&v=4" width=115><br><sub>Julia de Moura Rosa</sub>](https://github.com/JuliaRosa0401) |
| :---: | :---: |