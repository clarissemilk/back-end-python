#!/usr/bin/env python3
"""
Exemplos práticos dos principais decoradores Python
Execute este arquivo para ver todos os exemplos funcionando
"""

from functools import wraps, lru_cache, singledispatch
from contextlib import contextmanager
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import time


print("=" * 70)
print("🎯 GUIA PRÁTICO: DECORADORES PYTHON")
print("=" * 70)


# ============================================================================
# 1. @property e @setter
# ============================================================================
print("\n" + "=" * 70)
print("1️⃣ @property e @setter - Encapsulamento com Validação")
print("=" * 70)

class Produto:
    def __init__(self, nome, preco):
        self._nome = None
        self._preco = None
        self.nome = nome  # Usa setter
        self.preco = preco  # Usa setter
    
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, value):
        if not value or len(value) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        self._nome = value.title()
    
    @property
    def preco(self):
        return self._preco
    
    @preco.setter
    def preco(self, value):
        if value < 0:
            raise ValueError("Preço não pode ser negativo")
        self._preco = value
    
    @property
    def preco_com_desconto(self):
        """Propriedade calculada (read-only)"""
        return self._preco * 0.9

# Teste
try:
    p = Produto("notebook", 1000)
    print(f"✅ Produto criado: {p.nome}, Preço: R$ {p.preco:.2f}")
    print(f"   Preço com desconto: R$ {p.preco_com_desconto:.2f}")
    
    p.preco = 900
    print(f"✅ Preço atualizado: R$ {p.preco:.2f}")
    
    # p.preco = -100  # ❌ Erro
    # p.nome = "ab"  # ❌ Erro
except ValueError as e:
    print(f"❌ Erro: {e}")


# ============================================================================
# 2. @staticmethod
# ============================================================================
print("\n" + "=" * 70)
print("2️⃣ @staticmethod - Métodos que não precisam de instância")
print("=" * 70)

class Calculadora:
    @staticmethod
    def somar(a, b):
        return a + b
    
    @staticmethod
    def multiplicar(a, b):
        return a * b
    
    @staticmethod
    def potencia(base, expoente):
        return base ** expoente

# Uso sem instância
print(f"✅ 5 + 3 = {Calculadora.somar(5, 3)}")
print(f"✅ 4 * 7 = {Calculadora.multiplicar(4, 7)}")
print(f"✅ 2^8 = {Calculadora.potencia(2, 8)}")


# ============================================================================
# 3. @classmethod
# ============================================================================
print("\n" + "=" * 70)
print("3️⃣ @classmethod - Factory Methods")
print("=" * 70)

class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
    
    @classmethod
    def criar_maior_idade(cls, nome):
        """Factory: cria pessoa com 18 anos"""
        return cls(nome, 18)
    
    @classmethod
    def criar_do_dict(cls, dados):
        """Factory: cria pessoa a partir de dicionário"""
        return cls(dados['nome'], dados['idade'])
    
    def __repr__(self):
        return f"Pessoa(nome='{self.nome}', idade={self.idade})"

# Uso
p1 = Pessoa("João", 25)
p2 = Pessoa.criar_maior_idade("Maria")
p3 = Pessoa.criar_do_dict({"nome": "Pedro", "idade": 30})

print(f"✅ {p1}")
print(f"✅ {p2}")
print(f"✅ {p3}")


# ============================================================================
# 4. @contextmanager
# ============================================================================
print("\n" + "=" * 70)
print("4️⃣ @contextmanager - Gerenciamento de Recursos")
print("=" * 70)

@contextmanager
def temporizador(nome):
    """Mede tempo de execução"""
    inicio = time.time()
    print(f"⏱️ Iniciando: {nome}")
    yield
    fim = time.time()
    print(f"✅ Concluído: {nome} em {fim - inicio:.2f}s")

with temporizador("Operação pesada"):
    time.sleep(0.5)
    print("   ⚪ Executando operação...")


# ============================================================================
# 5. @functools.wraps
# ============================================================================
print("\n" + "=" * 70)
print("5️⃣ @functools.wraps - Preservar Metadados")
print("=" * 70)

# ❌ SEM @wraps
def decorador_sem_wraps(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

# ✅ COM @wraps
def decorador_com_wraps(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@decorador_sem_wraps
def minha_funcao():
    """Esta é minha função"""
    pass

@decorador_com_wraps
def minha_funcao2():
    """Esta é minha função"""
    pass

print(f"❌ Sem @wraps: nome='{minha_funcao.__name__}', doc='{minha_funcao.__doc__}'")
print(f"✅ Com @wraps: nome='{minha_funcao2.__name__}', doc='{minha_funcao2.__doc__}'")


# ============================================================================
# 6. @functools.lru_cache
# ============================================================================
print("\n" + "=" * 70)
print("6️⃣ @functools.lru_cache - Cache de Resultados")
print("=" * 70)

# Função custosa
@lru_cache(maxsize=128)
def calcular_potencia(base, expoente):
    """Calcula potência (cacheia resultados)"""
    print(f"   🔄 Calculando {base}^{expoente}...")
    return base ** expoente

print("Primeira chamada (calcula):")
resultado1 = calcular_potencia(2, 10)
print(f"   Resultado: {resultado1}")

print("\nSegunda chamada (usa cache):")
resultado2 = calcular_potencia(2, 10)
print(f"   Resultado: {resultado2}")


# ============================================================================
# 7. @functools.singledispatch
# ============================================================================
print("\n" + "=" * 70)
print("7️⃣ @functools.singledispatch - Polimorfismo de Funções")
print("=" * 70)

@singledispatch
def processar(dados):
    return f"Tipo genérico: {type(dados).__name__}"

@processar.register
def _(dados: str):
    return f"String: {dados.upper()}"

@processar.register
def _(dados: int):
    return f"Inteiro: {dados * 2}"

@processar.register
def _(dados: list):
    return f"Lista: {len(dados)} itens"

print(f"✅ {processar('hello')}")
print(f"✅ {processar(42)}")
print(f"✅ {processar([1, 2, 3, 4])}")
print(f"✅ {processar(3.14)}")


# ============================================================================
# 8. @dataclass
# ============================================================================
print("\n" + "=" * 70)
print("8️⃣ @dataclass - Classes de Dados Automáticas")
print("=" * 70)

@dataclass
class Aluno:
    nome: str
    idade: int
    nota: float = 0.0
    cursos: list = field(default_factory=list)

a1 = Aluno("João", 20, 9.5)
a2 = Aluno("João", 20, 9.5)
a3 = Aluno("Maria", 22, 8.0)

print(f"✅ {a1}")
print(f"✅ a1 == a2: {a1 == a2}")
print(f"✅ a1 == a3: {a1 == a3}")


# ============================================================================
# 9. @abstractmethod
# ============================================================================
print("\n" + "=" * 70)
print("9️⃣ @abstractmethod - Classes Abstratas")
print("=" * 70)

class Animal(ABC):
    @abstractmethod
    def fazer_som(self):
        pass
    
    @abstractmethod
    def mover(self):
        pass

class Cachorro(Animal):
    def fazer_som(self):
        return "Au au!"
    
    def mover(self):
        return "Correndo"

class Gato(Animal):
    def fazer_som(self):
        return "Miau!"
    
    def mover(self):
        return "Andando silenciosamente"

c = Cachorro()
g = Gato()

print(f"✅ Cachorro: {c.fazer_som()}, {c.mover()}")
print(f"✅ Gato: {g.fazer_som()}, {g.mover()}")


# ============================================================================
# 10. Decorador Customizado: Medir Tempo
# ============================================================================
print("\n" + "=" * 70)
print("🔟 Decorador Customizado: Medir Tempo")
print("=" * 70)

def medir_tempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fim = time.time()
        print(f"   ⏱️ {func.__name__} executou em {fim - inicio:.4f}s")
        return resultado
    return wrapper

@medir_tempo
def operacao_lenta():
    time.sleep(0.1)
    return "Concluído"

resultado = operacao_lenta()
print(f"   ✅ Resultado: {resultado}")


# ============================================================================
# 11. Decorador Customizado: Retry
# ============================================================================
print("\n" + "=" * 70)
print("1️⃣1️⃣ Decorador Customizado: Retry")
print("=" * 70)

def retry(max_tentativas=3):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for tentativa in range(max_tentativas):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if tentativa == max_tentativas - 1:
                        raise
                    print(f"   ⚠️ Tentativa {tentativa + 1} falhou: {e}")
                    time.sleep(0.1)
        return wrapper
    return decorador

@retry(max_tentativas=3)
def operacao_instavel():
    import random
    if random.random() < 0.6:
        raise ValueError("Falha aleatória")
    return "Sucesso!"

try:
    resultado = operacao_instavel()
    print(f"   ✅ {resultado}")
except ValueError as e:
    print(f"   ❌ Falhou após 3 tentativas: {e}")


# ============================================================================
# RESUMO
# ============================================================================
print("\n" + "=" * 70)
print("📚 RESUMO DOS DECORADORES")
print("=" * 70)
print("""
✅ @property/@setter      - Encapsulamento e validação
✅ @staticmethod          - Métodos sem instância
✅ @classmethod          - Factory methods
✅ @contextmanager       - Gerenciamento de recursos
✅ @functools.wraps      - Preservar metadados
✅ @functools.lru_cache  - Cache de resultados
✅ @functools.singledispatch - Polimorfismo de funções
✅ @dataclass            - Classes de dados automáticas
✅ @abstractmethod       - Classes abstratas
✅ Decoradores customizados - Criar seus próprios

💡 Dica: Comece dominando @property, @staticmethod, @classmethod e @contextmanager!
""")

