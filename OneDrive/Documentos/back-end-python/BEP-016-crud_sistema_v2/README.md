# Sistema CRUD de Gerenciamento de Alunos - Versão 2 (Orientada a Objetos - Simplificada)

Esta é a versão 2 do sistema CRUD, desenvolvida usando **Programação Orientada a Objetos (POO) básica**.

## 📚 Conceitos Aplicados

Este sistema demonstra os conceitos básicos aprendidos nas BEP-017 a BEP-022:

### BEP-017: Fundamentos de POO
- **Classes**: `Aluno`, `DatabaseManager`, `AlunoRepository`, `Menu`, `SistemaAlunos`
- **Objetos**: Instâncias das classes representando entidades do sistema
- **Atributos e Métodos**: Cada classe possui seus próprios atributos e comportamentos

### BEP-018: Criando e Instanciando Classes
- **Construtores (`__init__`)**: Todas as classes têm construtores apropriados
- **Instanciação**: Objetos são criados e utilizados em todo o sistema

### BEP-019: Encapsulamento
- **Validação**: Validações nos construtores e métodos garantem integridade dos dados
- **Métodos de atualização**: Método `atualizar()` para modificar dados

### BEP-021: Composição e Associação
- **Composição**: `SistemaAlunos` tem `AlunoRepository` e `Menu`
- **Associação**: `AlunoRepository` usa `DatabaseManager`

### BEP-022: Tratamento de Exceções
- **Try-except básico**: Tratamento de exceções em todos os métodos
- **Exceções simples**: Uso de `ValueError` e `Exception` padrão do Python

## 🏗️ Estrutura do Sistema

```
crud_sistema_v2/
├── __init__.py          # Inicialização do pacote
├── models.py            # Classe Aluno (entidade)
├── database.py          # Classe DatabaseManager (gerenciamento de BD)
├── repository.py        # Classe AlunoRepository (operações CRUD)
├── menu.py              # Classe Menu (interface)
├── sistema.py           # Classe SistemaAlunos (orquestrador)
├── exceptions.py        # Exceções customizadas (simplificadas)
└── README.md            # Este arquivo
```

## 🔑 Principais Classes

### `Aluno` (models.py)
- Representa a entidade Aluno
- Validação automática de dados no construtor
- Métodos: `atualizar()`, `__str__()`

### `DatabaseManager` (database.py)
- Gerencia conexões com banco de dados
- Métodos: `conectar()`, `fechar()`, `get_cursor()`

### `AlunoRepository` (repository.py)
- Operações CRUD no banco de dados
- Composição com `DatabaseManager`
- Métodos: `criar()`, `buscar_por_id()`, `listar_todos()`, `atualizar()`, `remover()`

### `Menu` (menu.py)
- Interface do usuário
- Métodos estáticos (`@staticmethod`) para exibição
- Formatação de dados

### `SistemaAlunos` (sistema.py)
- Orquestra todo o sistema
- Composição: tem `AlunoRepository` e `Menu`
- Tratamento de exceções centralizado

## 🚀 Como Usar

### ⚙️ Ambiente Virtual (venv) - Opcional mas Recomendado

**📌 Importante:** Este projeto usa apenas a biblioteca padrão do Python (`sqlite3`), então **tecnicamente não é obrigatório** usar um ambiente virtual.

**Porém, é uma boa prática usar venv porque:**
- ✅ Ensina boas práticas desde o início
- ✅ Prepara para projetos futuros que terão dependências externas
- ✅ Isola o ambiente do sistema operacional
- ✅ É uma prática profissional padrão em Python

**Como criar e usar um venv (opcional):**

```bash
# 1. Criar o ambiente virtual (na raiz do projeto ou na pasta do sistema)
python3 -m venv venv

# 2. Ativar o ambiente virtual
# No Linux/Mac:
source venv/bin/activate

# No Windows:
# venv\Scripts\activate

# 3. Executar o sistema normalmente
python3 -m BEP-016.crud_sistema_v2.sistema

# 4. Desativar quando terminar (opcional)
deactivate
```

**💡 Dica:** Se você não usar venv, pode executar diretamente. O sistema funcionará normalmente!

### Execução do Sistema

**⚠️ IMPORTANTE:** Este sistema deve ser executado como módulo Python devido aos imports relativos.

```bash
# Na raiz do projeto (aulas/)
python3 -m BEP-016.crud_sistema_v2.sistema
```

**Nota:** Se você estiver usando `python` ao invés de `python3`, use:
```bash
python -m BEP-016.crud_sistema_v2.sistema
```

### 📚 Entendendo Imports Relativos e Módulos Python

#### O que são Imports Relativos?

No código deste sistema, você verá imports assim:

```python
# Em sistema.py
from .database import DatabaseManager
from .repository import AlunoRepository
from .menu import Menu
from .models import Aluno
```

O **ponto (`.`)** no início indica um **import relativo**. Isso significa:
- `from .database import ...` = "importe do módulo `database` que está na **mesma pasta**"
- `from ..pasta import ...` = "importe da pasta **pai**"
- `from .models import ...` = "importe do módulo `models` que está na **mesma pasta**"

#### Por que não funciona executar diretamente?

Se você tentar executar o arquivo diretamente:

```bash
# ❌ ISSO NÃO FUNCIONA:
python3 BEP-016/crud_sistema_v2/sistema.py
```

Você receberá um erro: `ImportError: attempted relative import with no known parent package`

**Por quê?**
- Quando você executa um arquivo Python diretamente, o Python **não sabe** que ele faz parte de um pacote
- O Python trata o arquivo como um **script isolado**
- Sem contexto de pacote, o ponto (`.`) não tem significado - não há "pasta atual" definida
- O Python não consegue encontrar `database.py`, `models.py`, etc.

#### Como funciona com `python3 -m`?

Quando você usa `python3 -m`:

```bash
# ✅ ISSO FUNCIONA:
python3 -m BEP-016.crud_sistema_v2.sistema
```

O Python:
1. **Entende** que `BEP-016.crud_sistema_v2` é um **pacote** (pasta com `__init__.py`)
2. **Define o contexto** para os imports relativos
3. O ponto (`.`) agora significa "mesma pasta do pacote"
4. Consegue encontrar `database.py`, `models.py`, etc. corretamente

#### Analogia Simples

- **Executar diretamente:** É como pedir "pegue o arquivo da pasta ao lado" sem saber onde você está
- **Executar como módulo:** É como dizer "estou na pasta `BEP-016/crud_sistema_v2`, pegue o arquivo da pasta ao lado"

#### Por que o nome da pasta tem hífen?

**⚠️ Observação importante:** O nome da pasta `BEP-016` contém um **hífen (`-`)**, o que causa uma limitação:

- **Não é possível** fazer imports absolutos como `from BEP-016.crud_sistema_v2 import ...` porque hífens não são válidos em nomes de módulos Python
- Por isso, usamos **imports relativos** (`from .database import ...`)
- E por isso precisamos executar como módulo com `python3 -m`

**💡 Dica para projetos futuros:** Use **underscore (`_`)** em vez de hífen nos nomes de pastas que contêm código Python (ex: `BEP_016` em vez de `BEP-016`). Isso permite usar tanto imports relativos quanto absolutos!

#### Resumo

| Forma de Executar | Funciona? | Por quê? |
|-------------------|-----------|----------|
| `python3 sistema.py` | ❌ Não | Python não sabe que é um pacote |
| `python3 -m BEP-016.crud_sistema_v2.sistema` | ✅ Sim | Python entende a estrutura do pacote |

#### Alternativa (se não houvesse hífen)

Se a pasta se chamasse `BEP_016` (com underscore), você poderia usar imports absolutos:

```python
# Em vez de imports relativos:
from .database import DatabaseManager

# Poderia usar imports absolutos:
from BEP_016.crud_sistema_v2.database import DatabaseManager
```

E poderia executar diretamente (embora ainda seja melhor usar `-m` para manter a estrutura de pacote).

### Uso das Classes Individualmente

**Nota:** Devido ao hífen no nome da pasta `BEP-016`, a forma mais simples é executar o sistema completo ou trabalhar dentro da pasta `crud_sistema_v2/` diretamente.

# Criar aluno
aluno = Aluno(nome="João Silva", idade=20, curso="Python", nota=9.5)

# Gerenciar banco
db = DatabaseManager('alunos_v2.db')
db.conectar()

# Operações CRUD
repo = AlunoRepository(db)
aluno_criado = repo.criar(aluno)

# Fechar conexão
db.fechar()
```

## 🔄 Diferenças da Versão 1 (Procedural)

| Aspecto | Versão 1 (Procedural) | Versão 2 (OO Simplificada) |
|---------|----------------------|----------------------------|
| **Estrutura** | Funções em módulos | Classes e objetos |
| **Dados** | Tuplas e dicionários | Objetos `Aluno` |
| **Validação** | Manual em cada função | Automática na classe |
| **Organização** | Funções separadas | Classes com métodos |
| **Exceções** | Genéricas | Try-except básico |
| **Composição** | Não aplicada | Repository e Manager |
| **Reutilização** | Funções | Classes reutilizáveis |

## 📝 Exemplo de Uso Completo

**Nota:** Devido ao hífen no nome da pasta `BEP-016`, a forma mais simples é executar o sistema diretamente:

```bash
# Executar o sistema completo
python -m BEP-016.crud_sistema_v2.sistema
```

Ou, se quiser usar as classes em um script próprio, você pode trabalhar dentro da pasta `BEP-016/crud_sistema_v2/`:

```python
# Dentro da pasta BEP-016/crud_sistema_v2/
from models import Aluno
from database import DatabaseManager
from repository import AlunoRepository

# Criar aluno
aluno = Aluno(nome="Maria", idade=22, curso="Python", nota=8.5)

# Gerenciar banco
db = DatabaseManager('alunos_v2.db')
db.conectar()

# Operações CRUD
repo = AlunoRepository(db)
aluno_criado = repo.criar(aluno)

# Buscar aluno
aluno_encontrado = repo.buscar_por_id(1)

# Listar todos
todos = repo.listar_todos()

# Atualizar
aluno_encontrado.atualizar(nota=9.0)
repo.atualizar(aluno_encontrado)

# Remover
repo.remover(1)

db.fechar()
```

## 🎯 Benefícios da Versão OO

1. **Organização**: Código agrupado em classes lógicas
2. **Reutilização**: Classes podem ser usadas em outros contextos
3. **Manutenibilidade**: Código organizado e fácil de modificar
4. **Validação**: Dados validados automaticamente na classe
5. **Clareza**: Código mais expressivo e fácil de entender

## ⚠️ Versão Simplificada

Esta é uma **versão simplificada** que usa apenas conceitos básicos de OOP:
- ✅ Classes e objetos básicos
- ✅ Construtores e métodos simples
- ✅ Validação básica
- ✅ Composição simples
- ✅ Try-except básico
- ❌ Sem type hints complexos (`Optional[int]`, etc.)
- ❌ Sem decoradores avançados (`@contextmanager`, `@classmethod` complexo)
- ❌ Sem exceções customizadas complexas
- ❌ Sem conceitos avançados não vistos nas aulas

## 📚 Próximos Passos

Compare esta versão com a versão 1 (`BEP-016/crud_sistema/`) para entender as diferenças entre programação procedural e orientada a objetos!

Veja também os slides comparativos em `BEP-CRUD/` para uma análise detalhada das diferenças entre as duas versões.
