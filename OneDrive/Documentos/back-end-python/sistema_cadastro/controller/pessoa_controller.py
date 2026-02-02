from model.pessoa import Pessoa
from integracoes.cep_client import CepClient

class PessoaController:
    def __init__(self):
        self.pessoas = []
        self.proximo_id = 1

    def criar(self, nome, cep):
        endereco = CepClient.consultar(cep)

        if endereco is None:
            print("CEP inválido.")
            return

        pessoa = Pessoa(self.proximo_id, nome, cep, endereco)
        self.pessoas.append(pessoa)
        self.proximo_id += 1

        print("Pessoa cadastrada com sucesso!")

    def listar(self):
        return self.pessoas

    def atualizar(self, id, novo_nome, novo_cep):
        for pessoa in self.pessoas:
            if pessoa.id == id:
                endereco = CepClient.consultar(novo_cep)

                if endereco is None:
                    print("CEP inválido.")
                    return

                pessoa.nome = novo_nome
                pessoa.cep = novo_cep
                pessoa.endereco = endereco
                print("Pessoa atualizada com sucesso!")
                return

        print("Pessoa não encontrada.")

    def deletar(self, id):
        for pessoa in self.pessoas:
            if pessoa.id == id:
                self.pessoas.remove(pessoa)
                print("Pessoa removida com sucesso!")
                return

        print("Pessoa não encontrada.")


