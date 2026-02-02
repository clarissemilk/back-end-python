# Classe responsável pela interação com o usuário (View)
class PessoaView:

    @staticmethod
    def menu():
        print("\n1 - Cadastrar pessoa")
        print("2 - Listar pessoas")
        print("3 - Atualizar pessoa")
        print("4 - Remover pessoa")
        print("0 - Sair")

        return input("Escolha uma opção: ")

    @staticmethod
    def dados_pessoa():
        nome = input("Nome: ")
        cep = input("CEP: ")
        return nome, cep

    @staticmethod
    def mostrar_pessoas(pessoas):
        if not pessoas:
            print("Nenhuma pessoa cadastrada.")
            return

        for pessoa in pessoas:
            print(pessoa)


