from controller.pessoa_controller import PessoaController
from view.pessoa_view import PessoaView

controller = PessoaController()

while True:
    opcao = PessoaView.menu()

    if opcao == "1":
        nome, cep = PessoaView.dados_pessoa()
        controller.criar(nome, cep)

    elif opcao == "2":
        pessoas = controller.listar()
        PessoaView.mostrar_pessoas(pessoas)

    elif opcao == "3":
        id = int(input("ID da pessoa: "))
        nome, cep = PessoaView.dados_pessoa()
        controller.atualizar(id, nome, cep)

    elif opcao == "4":
        id = int(input("ID da pessoa: "))
        controller.deletar(id)

    elif opcao == "0":
        print("Encerrando...")
        break

    else:
        print("Opção inválida.")


