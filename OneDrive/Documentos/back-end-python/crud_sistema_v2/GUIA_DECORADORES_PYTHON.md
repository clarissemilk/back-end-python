# 🎯 Guia Completo: Decoradores Python Essenciais

## 📚 Índice

1. [Decoradores de Propriedades](#1-decoradores-de-propriedades)
   - `@property` e `@setter`
   - `@deleter`
2. [Decoradores de Métodos](#2-decoradores-de-métodos)
   - `@staticmethod`
   - `@classmethod`
3. [Decoradores de Contexto](#3-decoradores-de-contexto)
   - `@contextmanager`
4. [Decoradores de Função](#4-decoradores-de-função)
   - `@functools.wraps`
   - `@functools.lru_cache`
   - `@functools.singledispatch`
5. [Decoradores de Classe](#5-decoradores-de-classe)
   - `@dataclass`
   - `@abstractmethod` e `@abstractclassmethod`
6. [Decoradores de Validação](#6-decoradores-de-validação)
   - `@validator` (Pydantic)
7. [Criando Seus Próprios Decoradores](#7-criando-seus-próprios-decoradores)

---

## 1. Decoradores de Propriedades

### 🔹 `@property` e `@setter`

**O que faz:** Transforma métodos em propriedades acessíveis como atributos, com validação.

**Quando usar:** Quando você precisa de getters/setters com validação, mas quer sintaxe de atributo.

**Exemplo no nosso código (`models.py`):**

```python
class Aluno:
    def __init__(self, nome: str, idade: int = None):
        self._nome = None
        self._idade = None
        self.nome = nome  # Usa o setter
        self.idade = idade  # Usa o setter
    
    @property
    def nome(self) -> str:
        """Getter: retorna o nome"""
        return self._nome
    
    @nome.setter
    def nome(self, value: str):
        """Setter: valida e define o nome"""
        if not value or len(value.strip()) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        self._nome = value.strip()
    
    @property
    def idade(self) -> int:
        """Getter: retorna a idade"""
        return self._idade
    
    @idade.setter
    def idade(self, value: int):
        """Setter: valida e define a idade"""
        if value is not None and (value < 0 or value > 150):
            raise ValueError("Idade deve estar entre 0 e 150")
        self._idade = value

# Uso
aluno = Aluno("João Silva", 25)
print(aluno.nome)  # "João Silva" - acessa como atributo
aluno.nome = "Maria"  # Usa setter com validação
aluno.idade = 200  # ❌ Erro: ValueError
```

**Vantagens:**
- ✅ Sintaxe limpa (acesso como atributo)
- ✅ Validação automática
- ✅ Encapsulamento mantido
- ✅ Pode calcular valores dinamicamente

**Exemplo: Propriedade Calculada**

```python
class Retangulo:
    def __init__(self, largura, altura):
        self._largura = largura
        self._altura = altura
    
    @property
    def area(self):
        """Calcula área dinamicamente"""
        return self._largura * self._altura
    
    @property
    def perimetro(self):
        """Calcula perímetro dinamicamente"""
        return 2 * (self._largura + self._altura)

r = Retangulo(5, 3)
print(r.area)  # 15 - calculado automaticamente
print(r.perimetro)  # 16 - calculado automaticamente
```

### 🔹 `@deleter`

**O que faz:** Define comportamento quando `del` é usado na propriedade.

**Quando usar:** Quando você precisa limpar recursos ao deletar uma propriedade.

**Exemplo:**

```python
class Arquivo:
    def __init__(self, nome):
        self._nome = nome
        self._arquivo = open(nome, 'w')
    
    @property
    def arquivo(self):
        return self._arquivo
    
    @arquivo.deleter
    def arquivo(self):
        """Fecha arquivo ao deletar"""
        if self._arquivo:
            self._arquivo.close()
            self._arquivo = None
            print("Arquivo fechado")

a = Arquivo("teste.txt")
del a.arquivo  # Fecha o arquivo automaticamente
```

---

## 2. Decoradores de Métodos

### 🔹 `@staticmethod`

**O que faz:** Define um método que não precisa de instância (`self`) nem da classe (`cls`).

**Quando usar:** Para funções utilitárias relacionadas à classe, mas que não precisam acessar dados da instância.

**Exemplo no nosso código (`menu.py`):**

```python
class Menu:
    @staticmethod
    def exibir_menu():
        """Não precisa de self - é uma função utilitária"""
        print("="*50)
        print("🎓 SISTEMA DE GERENCIAMENTO DE ALUNOS")
        print("="*50)
        # ... menu ...

    @staticmethod
    def exibir_cabecalho(titulo: str):
        """Função utilitária para exibir cabeçalhos"""
        print(f"\n{titulo}")
        print("-" * len(titulo))

# Uso - pode chamar sem instanciar
Menu.exibir_menu()
Menu.exibir_cabecalho("Título")
```

**Vantagens:**
- ✅ Não precisa criar instância
- ✅ Organiza funções relacionadas à classe
- ✅ Não acessa `self` ou `cls`

**Comparação:**

```python
class Calculadora:
    # ❌ Método de instância (desnecessário)
    def somar(self, a, b):
        return a + b  # self não é usado!
    
    # ✅ Método estático (correto)
    @staticmethod
    def somar(a, b):
        return a + b

# Uso
calc = Calculadora()
calc.somar(2, 3)  # Funciona, mas desnecessário

Calculadora.somar(2, 3)  # ✅ Melhor: sem instância
```

### 🔹 `@classmethod`

**O que faz:** Define um método que recebe a classe (`cls`) como primeiro parâmetro, não a instância.

**Quando usar:** Para métodos alternativos de criação de objetos (factory methods) ou métodos que precisam acessar a classe.

**Exemplo no nosso código (`models.py`):**

```python
class Aluno:
    def __init__(self, nome: str, idade: int = None):
        self._nome = nome
        self._idade = idade
    
    @classmethod
    def from_tuple(cls, data: tuple):
        """
        Factory method: cria Aluno a partir de tupla
        Útil para criar objetos a partir de dados do banco
        """
        if len(data) == 6:
            return cls(
                id=data[0],
                nome=data[1],
                idade=data[2],
                curso=data[3],
                nota=data[4],
                data_cadastro=data[5]
            )
        raise ValueError("Tupla inválida")

# Uso
dados_banco = (1, "João", 25, "Python", 9.5, "2024-01-01")
aluno = Aluno.from_tuple(dados_banco)  # Cria usando classmethod
```

**Exemplo: Factory Methods**

```python
class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
    
    @classmethod
    def criar_maior_idade(cls, nome):
        """Factory: cria pessoa com 18 anos"""
        return cls(nome, 18)
    
    @classmethod
    def criar_do_arquivo(cls, arquivo):
        """Factory: cria pessoa a partir de arquivo"""
        dados = arquivo.read().split(',')
        return cls(dados[0], int(dados[1]))

# Uso
p1 = Pessoa.criar_maior_idade("João")
p2 = Pessoa.criar_do_arquivo(arquivo)
```

**Comparação: `@staticmethod` vs `@classmethod`**

```python
class Data:
    def __init__(self, dia, mes, ano):
        self.dia = dia
        self.mes = mes
        self.ano = ano
    
    @staticmethod
    def validar(dia, mes, ano):
        """Não precisa da classe - função utilitária"""
        return 1 <= dia <= 31 and 1 <= mes <= 12
    
    @classmethod
    def hoje(cls):
        """Precisa da classe para criar instância"""
        from datetime import date
        hoje = date.today()
        return cls(hoje.day, hoje.month, hoje.year)

# Uso
Data.validar(15, 3, 2024)  # staticmethod
data_hoje = Data.hoje()  # classmethod cria instância
```

---

## 3. Decoradores de Contexto

### 🔹 `@contextmanager`

**O que faz:** Cria context managers usando funções geradoras.

**Quando usar:** Para garantir limpeza de recursos (arquivos, conexões, transações).

**Exemplo no nosso código (`database.py`):**

```python
from contextlib import contextmanager

class DatabaseManager:
    @contextmanager
    def get_cursor(self):
        """Garante commit/rollback automático"""
        try:
            cursor = self._connection.cursor()
            yield cursor  # Retorna cursor
            self._connection.commit()  # Sucesso: salva
        except:
            self._connection.rollback()  # Erro: desfaz
            raise

# Uso
with db.get_cursor() as cursor:
    cursor.execute("INSERT ...")
    # Commit automático se sucesso
    # Rollback automático se erro
```

**Ver explicação detalhada em:** `EXPLICACAO_CONTEXTMANAGER.md`

---

## 4. Decoradores de Função

### 🔹 `@functools.wraps`

**O que faz:** Preserva metadados da função original (nome, docstring) ao criar decoradores.

**Quando usar:** Sempre que criar um decorador customizado.

**Exemplo:**

```python
from functools import wraps

# ❌ SEM @wraps
def meu_decorador(func):
    def wrapper(*args, **kwargs):
        print("Antes")
        resultado = func(*args, **kwargs)
        print("Depois")
        return resultado
    return wrapper

@meu_decorador
def minha_funcao():
    """Esta é minha função"""
    pass

print(minha_funcao.__name__)  # "wrapper" ❌ Perdeu o nome original!
print(minha_funcao.__doc__)  # None ❌ Perdeu a docstring!

# ✅ COM @wraps
def meu_decorador_correto(func):
    @wraps(func)  # Preserva metadados
    def wrapper(*args, **kwargs):
        print("Antes")
        resultado = func(*args, **kwargs)
        print("Depois")
        return resultado
    return wrapper

@meu_decorador_correto
def minha_funcao2():
    """Esta é minha função"""
    pass

print(minha_funcao2.__name__)  # "minha_funcao2" ✅
print(minha_funcao2.__doc__)  # "Esta é minha função" ✅
```

### 🔹 `@functools.lru_cache`

**O que faz:** Cacheia resultados de funções (memoização) para evitar recálculos.

**Quando usar:** Para funções custosas que são chamadas repetidamente com mesmos argumentos.

**Exemplo:**

```python
from functools import lru_cache

# ❌ SEM cache (lento)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# fibonacci(40) demora muito! (chamadas repetidas)

# ✅ COM cache (rápido)
@lru_cache(maxsize=128)
def fibonacci_cache(n):
    if n < 2:
        return n
    return fibonacci_cache(n-1) + fibonacci_cache(n-2)

# fibonacci_cache(40) é rápido! (cacheia resultados)
```

**Exemplo Prático:**

```python
@lru_cache(maxsize=100)
def calcular_imposto(valor, taxa):
    """Calcula imposto (cacheia para valores repetidos)"""
    print(f"Calculando imposto para {valor}...")
    return valor * taxa / 100

calcular_imposto(1000, 10)  # Calcula
calcular_imposto(1000, 10)  # Usa cache (não calcula novamente)
```

### 🔹 `@functools.singledispatch`

**O que faz:** Permite funções com comportamento diferente baseado no tipo do primeiro argumento (polimorfismo).

**Quando usar:** Quando você precisa de funções que se comportam diferente por tipo.

**Exemplo:**

```python
from functools import singledispatch

@singledispatch
def processar(dados):
    """Função base - tipo genérico"""
    print(f"Processando tipo genérico: {type(dados)}")

@processar.register
def _(dados: str):
    """Processa strings"""
    print(f"Processando string: {dados.upper()}")

@processar.register
def _(dados: int):
    """Processa inteiros"""
    print(f"Processando inteiro: {dados * 2}")

@processar.register
def _(dados: list):
    """Processa listas"""
    print(f"Processando lista: {len(dados)} itens")

# Uso
processar("hello")  # "Processando string: HELLO"
processar(42)  # "Processando inteiro: 84"
processar([1, 2, 3])  # "Processando lista: 3 itens"
processar(3.14)  # "Processando tipo genérico: <class 'float'>"
```

---

## 5. Decoradores de Classe

### 🔹 `@dataclass`

**O que faz:** Gera automaticamente `__init__`, `__repr__`, `__eq__`, etc. para classes simples.

**Quando usar:** Para classes que são principalmente containers de dados.

**Exemplo:**

```python
from dataclasses import dataclass, field

# ❌ SEM @dataclass (muito código repetitivo)
class Pessoa:
    def __init__(self, nome, idade, email):
        self.nome = nome
        self.idade = idade
        self.email = email
    
    def __repr__(self):
        return f"Pessoa(nome={self.nome}, idade={self.idade})"
    
    def __eq__(self, other):
        return (self.nome == other.nome and 
                self.idade == other.idade)

# ✅ COM @dataclass (automático)
@dataclass
class Pessoa:
    nome: str
    idade: int
    email: str = ""  # Valor padrão
    amigos: list = field(default_factory=list)  # Lista vazia

# Uso
p1 = Pessoa("João", 25, "joao@email.com")
p2 = Pessoa("João", 25, "joao@email.com")
print(p1)  # Pessoa(nome='João', idade=25, email='joao@email.com')
print(p1 == p2)  # True (comparação automática)
```

**Vantagens:**
- ✅ Menos código boilerplate
- ✅ `__repr__`, `__eq__`, `__hash__` automáticos
- ✅ Type hints integrados
- ✅ Valores padrão fáceis

### 🔹 `@abstractmethod` e `@abstractclassmethod`

**O que faz:** Define métodos que devem ser implementados por subclasses (classe abstrata).

**Quando usar:** Para criar interfaces/contratos que subclasses devem seguir.

**Exemplo:**

```python
from abc import ABC, abstractmethod

class Animal(ABC):  # Classe abstrata
    @abstractmethod
    def fazer_som(self):
        """Toda subclasse DEVE implementar"""
        pass
    
    @abstractmethod
    def mover(self):
        """Toda subclasse DEVE implementar"""
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

# Uso
c = Cachorro()
print(c.fazer_som())  # "Au au!"

# ❌ Erro: não pode instanciar classe abstrata
# animal = Animal()  # TypeError!
```

---

## 6. Decoradores de Validação

### 🔹 `@validator` (Pydantic)

**O que faz:** Valida dados de entrada em modelos Pydantic.

**Quando usar:** Para validação robusta de dados em APIs, formulários, etc.

**Exemplo:**

```python
from pydantic import BaseModel, validator

class Aluno(BaseModel):
    nome: str
    idade: int
    nota: float
    
    @validator('nome')
    def validar_nome(cls, v):
        if len(v) < 3:
            raise ValueError('Nome deve ter pelo menos 3 caracteres')
        return v.title()  # Capitaliza
    
    @validator('idade')
    def validar_idade(cls, v):
        if not 0 <= v <= 150:
            raise ValueError('Idade deve estar entre 0 e 150')
        return v
    
    @validator('nota')
    def validar_nota(cls, v):
        if not 0 <= v <= 10:
            raise ValueError('Nota deve estar entre 0 e 10')
        return v

# Uso
try:
    aluno = Aluno(nome="joão", idade=25, nota=9.5)
    print(aluno.nome)  # "João" (capitalizado)
except ValueError as e:
    print(f"Erro: {e}")
```

---

## 7. Criando Seus Próprios Decoradores

### Exemplo 1: Decorador de Tempo

```python
from functools import wraps
import time

def medir_tempo(func):
    """Decorador que mede tempo de execução"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.time()
        resultado = func(*args, **kwargs)
        fim = time.time()
        print(f"{func.__name__} executou em {fim - inicio:.2f}s")
        return resultado
    return wrapper

@medir_tempo
def processar_dados():
    time.sleep(1)
    return "Processado"

processar_dados()  # "processar_dados executou em 1.00s"
```

### Exemplo 2: Decorador de Retry

```python
from functools import wraps
import time

def retry(max_tentativas=3, delay=1):
    """Decorador que tenta novamente em caso de erro"""
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for tentativa in range(max_tentativas):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if tentativa == max_tentativas - 1:
                        raise
                    print(f"Tentativa {tentativa + 1} falhou: {e}. Tentando novamente...")
                    time.sleep(delay)
        return wrapper
    return decorador

@retry(max_tentativas=3, delay=2)
def conectar_api():
    # Simula conexão que pode falhar
    import random
    if random.random() < 0.7:
        raise ConnectionError("Falha na conexão")
    return "Conectado!"

conectar_api()  # Tenta até 3 vezes
```

### Exemplo 3: Decorador de Log

```python
from functools import wraps

def logar(func):
    """Decorador que loga chamadas de função"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"📝 Chamando {func.__name__} com args={args}, kwargs={kwargs}")
        resultado = func(*args, **kwargs)
        print(f"✅ {func.__name__} retornou: {resultado}")
        return resultado
    return wrapper

@logar
def somar(a, b):
    return a + b

somar(2, 3)
# 📝 Chamando somar com args=(2, 3), kwargs={}
# ✅ somar retornou: 5
```

---

## 📊 Tabela Comparativa: Quando Usar Cada Decorador

| Decorador | Quando Usar | Exemplo de Uso |
|-----------|-------------|----------------|
| `@property` | Getter/setter com validação | Atributos com validação |
| `@staticmethod` | Função utilitária da classe | `Menu.exibir_menu()` |
| `@classmethod` | Factory methods | `Aluno.from_tuple()` |
| `@contextmanager` | Gerenciamento de recursos | `with db.get_cursor()` |
| `@functools.wraps` | Criar decoradores | Preservar metadados |
| `@functools.lru_cache` | Funções custosas repetidas | Fibonacci, cálculos |
| `@dataclass` | Classes de dados simples | DTOs, modelos simples |
| `@abstractmethod` | Interfaces/contratos | Classes abstratas |

---

## 🎯 Resumo: Top 5 Decoradores Mais Importantes

1. **`@property`** - Essencial para encapsulamento e validação
2. **`@staticmethod`** - Organiza funções utilitárias
3. **`@classmethod`** - Factory methods e métodos de classe
4. **`@contextmanager`** - Gerenciamento seguro de recursos
5. **`@functools.wraps`** - Essencial ao criar decoradores

---

## 📚 Próximos Passos

- Pratique criando seus próprios decoradores
- Explore decoradores de bibliotecas (Flask, Django, FastAPI)
- Estude decoradores avançados: `@functools.total_ordering`, `@typing.overload`

---

**💡 Dica:** Comece dominando os 5 principais. Os outros você aprende conforme a necessidade!

