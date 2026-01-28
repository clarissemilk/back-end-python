from fastapi import Body, FastAPI #importando a feature fastapi

app = FastAPI(title="API Exemplo")

usuarios = [
    {"id": 1, "nome": "joão", "email": "joao@email.com"},
    {"id": 2, "nome": "Maria", "email": "maria@email.com"},
    {"id": 3, "nome": "José", "email": "jose@email.com"}
]

@app.get("/") # método da fastapi - ("/") isso é a rota da api
def raiz():
    return {"mensagem": "API funcionando!"}


@app.get("/usuarios")
def listar_usuarios():
        return usuarios

@app.post("/usuarios") # rota - Post recebe alguma coisa do site que tá chamando ele, ele guarda o dado que está recebendo
def criar_usuario(usuario: dict = Body(...)): # ===> usuario = {"id": 4, "nome": "Ana", "email": "ana@email"}
      id = usuario.get("id")
      nome = usuario.get("nome")  # dicionário está definido como usuário
      email = usuario.get("email")
      novo = {"id": id, "nome": nome, "email": email}
      usuarios.append(novo)
      return novo
