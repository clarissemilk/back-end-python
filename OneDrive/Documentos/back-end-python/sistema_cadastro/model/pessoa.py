# Classe que representa a entidade Pessoa (Model)
# Aqui ficam apenas os dados, sem regras de negócio

class Pessoa:
    def __init__(self, id, nome, cep, endereco):
        self.id = id
        self.nome = nome
        self.cep = cep
        self.endereco = endereco

    def __str__(self):
        return f"{self.id} - {self.nome} | {self.endereco}"

