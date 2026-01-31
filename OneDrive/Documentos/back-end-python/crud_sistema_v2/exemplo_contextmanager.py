#!/usr/bin/env python3
"""
Exemplos práticos do decorador @contextmanager
Demonstra como funciona e por que é útil
"""

from contextlib import contextmanager
import time


# ============================================
# EXEMPLO 1: Context Manager Simples
# ============================================
@contextmanager
def exemplo_simples():
    """
    Exemplo básico de context manager
    """
    print("🔵 Entrando no contexto (antes do yield)")
    yield "Valor retornado"
    print("🔴 Saindo do contexto (depois do yield)")


print("=" * 60)
print("EXEMPLO 1: Context Manager Simples")
print("=" * 60)
with exemplo_simples() as valor:
    print(f"   ⚪ Dentro do bloco 'with', valor = {valor}")
print()


# ============================================
# EXEMPLO 2: Temporizador
# ============================================
@contextmanager
def temporizador(nome_operacao):
    """
    Mede o tempo de execução de uma operação
    """
    inicio = time.time()
    print(f"⏱️ Iniciando: {nome_operacao}")
    yield
    fim = time.time()
    tempo_decorrido = fim - inicio
    print(f"✅ Concluído: {nome_operacao} em {tempo_decorrido:.2f} segundos")


print("=" * 60)
print("EXEMPLO 2: Temporizador")
print("=" * 60)
with temporizador("Processamento pesado"):
    # Simula operação que demora
    time.sleep(1)
    print("   ⚪ Executando operação...")
print()


# ============================================
# EXEMPLO 3: Gerenciamento de Recursos (Arquivo)
# ============================================
@contextmanager
def abrir_arquivo(nome_arquivo, modo='r'):
    """
    Abre arquivo e garante fechamento automático
    (Similar ao 'with open()' nativo)
    """
    print(f"📂 Abrindo arquivo: {nome_arquivo}")
    arquivo = open(nome_arquivo, modo)
    try:
        yield arquivo
    finally:
        arquivo.close()
        print(f"🔒 Arquivo fechado: {nome_arquivo}")


print("=" * 60)
print("EXEMPLO 3: Gerenciamento de Arquivo")
print("=" * 60)
try:
    with abrir_arquivo("teste.txt", "w") as f:
        f.write("Teste de escrita")
        print("   ⚪ Escrevendo no arquivo...")
except FileNotFoundError:
    print("   ⚠️ Arquivo não encontrado (exemplo)")
print()


# ============================================
# EXEMPLO 4: Transação de Banco (Similar ao nosso código)
# ============================================
class BancoSimulado:
    """Simula um banco de dados"""
    
    def __init__(self):
        self.transacoes = []
        self.rollback_feito = False
    
    @contextmanager
    def transacao(self):
        """
        Context manager para transações
        Garante commit em sucesso ou rollback em erro
        """
        print("🟢 Iniciando transação...")
        try:
            yield self
            # Se chegou aqui, não houve erro
            print("✅ Commit: Transação confirmada")
        except Exception as e:
            # Se houve erro, faz rollback
            self.rollback()
            print(f"❌ Rollback: Transação cancelada - {e}")
            raise
    
    def adicionar(self, item):
        """Adiciona item à transação"""
        self.transacoes.append(item)
        print(f"   ➕ Adicionado: {item}")
    
    def rollback(self):
        """Desfaz transação"""
        self.transacoes.clear()
        self.rollback_feito = True
        print("   🔄 Rollback executado")


print("=" * 60)
print("EXEMPLO 4: Transação de Banco (Sucesso)")
print("=" * 60)
banco = BancoSimulado()
with banco.transacao() as t:
    t.adicionar("Aluno 1")
    t.adicionar("Aluno 2")
    # Tudo certo, commit automático!
print(f"Transações finais: {banco.transacoes}")
print()


print("=" * 60)
print("EXEMPLO 4: Transação de Banco (Com Erro)")
print("=" * 60)
banco2 = BancoSimulado()
try:
    with banco2.transacao() as t:
        t.adicionar("Aluno 1")
        t.adicionar("Aluno 2")
        raise ValueError("Erro simulado!")
        # Não chega aqui
except ValueError:
    pass
print(f"Transações finais: {banco2.transacoes} (rollback feito)")
print()


# ============================================
# EXEMPLO 5: Comparação: Com vs Sem Context Manager
# ============================================
print("=" * 60)
print("EXEMPLO 5: Comparação")
print("=" * 60)

# ❌ SEM Context Manager
print("❌ SEM Context Manager:")
def operacao_sem_context():
    arquivo = open("teste2.txt", "w")
    try:
        arquivo.write("dados")
        # E se esquecer o close()?
        # E se der erro antes?
    finally:
        arquivo.close()  # Precisa lembrar manualmente

# ✅ COM Context Manager
print("✅ COM Context Manager:")
@contextmanager
def operacao_com_context():
    arquivo = open("teste2.txt", "w")
    try:
        yield arquivo
    finally:
        arquivo.close()  # Sempre fecha, mesmo com erro

with operacao_com_context() as f:
    f.write("dados")
    # Fecha automaticamente!

print("\n💡 Vantagem: Context Manager garante limpeza automática!")


# ============================================
# RESUMO
# ============================================
print("\n" + "=" * 60)
print("📚 RESUMO: @contextmanager")
print("=" * 60)
print("""
O decorador @contextmanager permite criar Context Managers de forma simples:

1. ANTES DO YIELD: Código executado ao ENTRAR no 'with'
2. YIELD: Retorna valor que será usado no 'as'
3. DEPOIS DO YIELD: Código executado ao SAIR do 'with'

Vantagens:
✅ Garante limpeza de recursos
✅ Código mais limpo e seguro
✅ Tratamento de erros automático
✅ Reutilizável

No nosso código (database.py):
- get_cursor() usa @contextmanager
- Garante commit em sucesso
- Garante rollback em erro
- Sempre limpa recursos
""")

