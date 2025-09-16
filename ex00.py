# Ler dois valores numéricos inteiros e apresentar o resultado da diferença do maior pelo menor valor.

# Ler dois valores inteiros
num1 = int(input("Digite o primeiro número: "))
num2 = int(input("Digite o segundo número: "))

# Verificar qual é o maior e calcular a diferença
if num1 > num2:
    diferenca = num1 - num2
else:
    diferenca = num2 - num1

# Mostrar resultado
print("A diferença do maior pelo menor valor é:", diferenca)
