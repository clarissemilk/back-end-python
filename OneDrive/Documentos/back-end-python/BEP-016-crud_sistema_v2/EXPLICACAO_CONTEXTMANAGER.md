# Explicação: Decorador `@contextmanager`

## 📚 O que é `@contextmanager`?

O `@contextmanager` é um **decorador** do módulo `contextlib` do Python que permite criar **Context Managers** (gerenciadores de contexto) de forma simples usando funções geradoras.

## 🔑 Conceito: Context Manager

Um **Context Manager** é um objeto que define o que acontece quando você entra e sai de um bloco de código usando `with`.

### Exemplo Clássico: Abrir Arquivo

```python
# Context Manager nativo do Python
with open('arquivo.txt', 'r') as f:
    conteudo = f.read()
    # Arquivo é automaticamente fechado ao sair do bloco
```

## 🎯 Por que Usar `@contextmanager`?

Sem `@contextmanager`, você precisaria criar uma classe com `__enter__` e `__exit__`:

```python
# Forma tradicional (mais verbosa)
class MeuContextManager:
    def __enter__(self):
        # Código executado ao entrar no 'with'
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Código executado ao sair do 'with'
        pass

# Uso
with MeuContextManager() as cm:
    # fazer algo
    pass
```

Com `@contextmanager`, você pode fazer isso com uma função:

```python
from contextlib import contextmanager

@contextmanager
def meu_context_manager():
    # Código antes do 'yield' = __enter__
    print("Entrando no contexto")
    yield "valor retornado"
    # Código depois do 'yield' = __exit__
    print("Saindo do contexto")

# Uso
with meu_context_manager() as valor:
    print(f"Valor: {valor}")
    # Saída:
    # Entrando no contexto
    # Valor: valor retornado
    # Saindo do contexto
```

## 💡 Como Funciona?

1. **Antes do `yield`**: Código executado ao **entrar** no `with` (equivalente a `__enter__`)
2. **`yield`**: Retorna o valor que será atribuído à variável após `as`
3. **Depois do `yield`**: Código executado ao **sair** do `with` (equivalente a `__exit__`)

## 🔍 Exemplo no Nosso Código

No arquivo `database.py`, temos:

```python
from contextlib import contextmanager

class DatabaseManager:
    @contextmanager
    def get_cursor(self):
        """
        Context manager para obter cursor do banco
        """
        try:
            # ANTES DO YIELD (entrada)
            if not self._connection:
                self.conectar()
            cursor = self._connection.cursor()
            
            # YIELD - retorna o cursor
            yield cursor
            
            # DEPOIS DO YIELD (saída)
            self._connection.commit()  # Salva alterações
            
        except sqlite3.Error as e:
            # Em caso de erro, faz rollback
            if self._connection:
                self._connection.rollback()
            raise ErroBancoDados("executar operação", e)
```

### Como é Usado:

```python
db = DatabaseManager()

# Uso do context manager
with db.get_cursor() as cursor:
    cursor.execute("INSERT INTO alunos ...")
    # Ao sair do 'with', commit() é chamado automaticamente!
    # Se houver erro, rollback() é chamado automaticamente!
```

## ✅ Vantagens do `@contextmanager`

### 1. **Garantia de Limpeza**
```python
# Sem context manager (perigoso)
cursor = db._connection.cursor()
cursor.execute("INSERT ...")
# E se der erro? E se esquecer o commit?

# Com context manager (seguro)
with db.get_cursor() as cursor:
    cursor.execute("INSERT ...")
    # Commit automático, rollback em caso de erro!
```

### 2. **Código Mais Limpo**
```python
# Sem context manager
try:
    cursor = db._connection.cursor()
    cursor.execute("...")
    db._connection.commit()
except:
    db._connection.rollback()
    raise

# Com context manager
with db.get_cursor() as cursor:
    cursor.execute("...")
    # Tudo automático!
```

### 3. **Reutilizável**
O mesmo context manager pode ser usado em vários lugares:

```python
# Em repository.py
def criar(self, aluno):
    with self._db_manager.get_cursor() as cursor:
        cursor.execute("INSERT ...")
        # Commit automático

def atualizar(self, aluno):
    with self._db_manager.get_cursor() as cursor:
        cursor.execute("UPDATE ...")
        # Commit automático
```

## 📊 Comparação: Com vs Sem `@contextmanager`

### ❌ Sem Context Manager

```python
def criar_aluno(self, aluno):
    try:
        cursor = self._connection.cursor()
        cursor.execute("INSERT ...")
        self._connection.commit()
    except sqlite3.Error as e:
        self._connection.rollback()
        raise
    finally:
        # Precisa lembrar de fechar cursor?
        pass
```

**Problemas:**
- Precisa lembrar de fazer commit manualmente
- Precisa lembrar de fazer rollback em caso de erro
- Código repetitivo em cada função
- Fácil esquecer tratamento de erros

### ✅ Com Context Manager

```python
@contextmanager
def get_cursor(self):
    try:
        cursor = self._connection.cursor()
        yield cursor
        self._connection.commit()
    except:
        self._connection.rollback()
        raise

def criar_aluno(self, aluno):
    with self.get_cursor() as cursor:
        cursor.execute("INSERT ...")
        # Commit e rollback automáticos!
```

**Vantagens:**
- Commit automático
- Rollback automático em caso de erro
- Código reutilizável
- Impossível esquecer tratamento de erros

## 🎓 Exemplos Práticos

### Exemplo 1: Temporizador

```python
from contextlib import contextmanager
import time

@contextmanager
def temporizador(nome):
    inicio = time.time()
    print(f"⏱️ Iniciando {nome}...")
    yield
    fim = time.time()
    print(f"✅ {nome} concluído em {fim - inicio:.2f} segundos")

# Uso
with temporizador("Processamento"):
    # Código que quer medir
    time.sleep(2)
```

### Exemplo 2: Mudar Diretório Temporariamente

```python
from contextlib import contextmanager
import os

@contextmanager
def mudar_diretorio(caminho):
    diretorio_original = os.getcwd()
    try:
        os.chdir(caminho)
        yield
    finally:
        os.chdir(diretorio_original)

# Uso
with mudar_diretorio("/tmp"):
    # Trabalha em /tmp
    print(os.getcwd())  # /tmp
# Volta automaticamente para o diretório original
```

### Exemplo 3: Transação de Banco de Dados (Nosso Caso)

```python
@contextmanager
def get_cursor(self):
    try:
        cursor = self._connection.cursor()
        yield cursor
        self._connection.commit()  # Sucesso: salva
    except:
        self._connection.rollback()  # Erro: desfaz
        raise

# Uso
with db.get_cursor() as cursor:
    cursor.execute("INSERT INTO alunos ...")
    # Se tudo der certo: commit()
    # Se der erro: rollback()
```

## 🔗 Relação com `with` Statement

O `@contextmanager` funciona em conjunto com o `with`:

```python
# Sintaxe
with contexto() as variavel:
    # código
    pass

# O que acontece:
# 1. Chama __enter__ (ou código antes do yield)
# 2. Atribui retorno a 'variavel'
# 3. Executa código do bloco
# 4. Chama __exit__ (ou código depois do yield)
```

## 📝 Resumo

| Aspecto | Explicação |
|---------|------------|
| **O que é** | Decorador que cria context managers com funções |
| **De onde vem** | Módulo `contextlib` do Python |
| **Para que serve** | Garantir que código de limpeza sempre execute |
| **Como funciona** | `yield` separa código de entrada e saída |
| **Vantagem** | Mais simples que criar classe com `__enter__`/`__exit__` |

## 🎯 No Nosso Projeto

No `DatabaseManager.get_cursor()`:
- ✅ **Entrada**: Cria cursor, garante conexão
- ✅ **Uso**: Retorna cursor para operações SQL
- ✅ **Saída**: Faz commit (sucesso) ou rollback (erro)
- ✅ **Garantia**: Sempre limpa recursos, mesmo com erros

Isso torna nosso código mais seguro e profissional! 🚀

