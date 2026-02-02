import requests

# Classe responsável por consultar a API ViaCEP
class CepClient:

    @staticmethod
    def consultar(cep):
        # Monta a URL da API com o CEP informado
        url = f"https://viacep.com.br/ws/{cep}/json/"
        resposta = requests.get(url)

        # Verifica se a requisição foi bem-sucedida
        if resposta.status_code == 200:
            dados = resposta.json()

            # Verifica se o CEP é inválido
            if "erro" in dados:
                return None

            # Retorna o endereço formatado
            return f"{dados['logradouro']} - {dados['bairro']} - {dados['localidade']}/{dados['uf']}"

        return None

