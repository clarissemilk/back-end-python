"""
Módulo Principal do Sistema
Aplica conceitos básicos de BEP-017 a BEP-022: Classes, Composição, Tratamento de Exceções simples
"""

from .database import DatabaseManager
from .repository import AlunoRepository
from .menu import Menu
from .models import Aluno


class SistemaAlunos:
    """
    Classe principal que orquestra o sistema
    Versão simplificada - apenas classes e métodos básicos
    """
    
    def __init__(self, db_name='alunos_v2.db'):
        """
        Inicializa o sistema
        
        Args:
            db_name: Nome do arquivo do banco de dados
        """
        # Composição: Sistema tem DatabaseManager e AlunoRepository
        self.db_manager = DatabaseManager(db_name)
        self.repository = AlunoRepository(self.db_manager)
        self.menu = Menu()
    
    def iniciar(self):
        """Inicia o sistema"""
        try:
            print("🚀 Iniciando Sistema de Gerenciamento de Alunos (Versão OO)...")
            self.db_manager.conectar()
            
            while True:
                self.menu.exibir_menu_principal()
                opcao = input("👉 Escolha uma opção: ").strip()
                
                try:
                    if opcao == '1':
                        self._cadastrar_aluno()
                    elif opcao == '2':
                        self._listar_alunos()
                    elif opcao == '3':
                        self._buscar_aluno()
                    elif opcao == '4':
                        self._atualizar_aluno()
                    elif opcao == '5':
                        self._remover_aluno()
                    elif opcao == '6':
                        self._mostrar_estatisticas()
                    elif opcao == '0':
                        print("\n👋 Obrigado por usar o sistema! Até logo!")
                        break
                    else:
                        print("❌ Opção inválida! Tente novamente.")
                except ValueError as e:
                    print(f"❌ Erro: {e}")
                except Exception as e:
                    print(f"❌ Erro inesperado: {e}")
                
                input("\n⏸️ Pressione Enter para continuar...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrompido pelo usuário.")
        except Exception as e:
            print(f"\n❌ Erro crítico: {e}")
        finally:
            self.db_manager.fechar()
    
    def _cadastrar_aluno(self):
        """Cadastra um novo aluno"""
        self.menu.exibir_cabecalho("📝 CADASTRO DE NOVO ALUNO")
        
        try:
            nome = input("Nome completo: ").strip()
            if not nome:
                print("❌ Nome é obrigatório!")
                return
            
            idade_str = input("Idade: ").strip()
            idade = int(idade_str) if idade_str else None
            
            curso = input("Curso: ").strip() or None
            
            nota_str = input("Nota (0-10): ").strip()
            nota = float(nota_str) if nota_str else None
            
            # Criar objeto Aluno (validação automática)
            aluno = Aluno(nome=nome, idade=idade, curso=curso, nota=nota)
            
            # Salvar no banco
            aluno_criado = self.repository.criar(aluno)
            if aluno_criado:
                print(f"✅ Aluno '{aluno_criado.nome}' cadastrado com sucesso! (ID: {aluno_criado.id})")
            else:
                print("❌ Erro ao cadastrar aluno!")
        
        except ValueError as e:
            print(f"❌ Erro: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    def _listar_alunos(self):
        """Lista todos os alunos"""
        try:
            alunos = self.repository.listar_todos()
            self.menu.exibir_lista_alunos(alunos)
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _buscar_aluno(self):
        """Busca alunos por nome"""
        nome_busca = input("\n🔍 Digite o nome para buscar: ").strip()
        if not nome_busca:
            print("❌ Digite um nome para buscar!")
            return
        
        try:
            alunos = self.repository.buscar_por_nome(nome_busca)
            self.menu.exibir_lista_alunos(alunos, f"RESULTADO DA BUSCA por '{nome_busca}'")
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    def _atualizar_aluno(self):
        """Atualiza dados de um aluno"""
        self.menu.exibir_cabecalho("✏️ ATUALIZAR DADOS DO ALUNO")
        
        try:
            # Listar alunos
            alunos = self.repository.listar_todos()
            if not alunos:
                print("📭 Nenhum aluno cadastrado!")
                return
            
            print("📋 Alunos disponíveis:")
            for aluno in alunos:
                print(f"  {aluno.id} - {aluno.nome}")
            
            aluno_id_str = input("\nDigite o ID do aluno: ").strip()
            if not aluno_id_str:
                print("❌ ID é obrigatório!")
                return
            
            aluno_id = int(aluno_id_str)
            aluno = self.repository.buscar_por_id(aluno_id)
            
            if not aluno:
                print(f"❌ Aluno com ID {aluno_id} não encontrado!")
                return
            
            print(f"\n📝 Atualizando dados de: {aluno.nome}")
            print("Deixe em branco para manter o valor atual")
            
            nome = input("Nome: ").strip() or None
            idade_str = input("Idade: ").strip()
            idade = int(idade_str) if idade_str else None
            curso = input("Curso: ").strip() or None
            nota_str = input("Nota: ").strip()
            nota = float(nota_str) if nota_str else None
            
            # Atualizar objeto
            aluno.atualizar(nome=nome, idade=idade, curso=curso, nota=nota)
            
            # Salvar no banco
            if self.repository.atualizar(aluno):
                print(f"✅ Aluno {aluno_id} atualizado com sucesso!")
            else:
                print("❌ Erro ao atualizar aluno!")
        
        except ValueError as e:
            print(f"❌ Erro: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    def _remover_aluno(self):
        """Remove um aluno"""
        self.menu.exibir_cabecalho("🗑️ REMOVER ALUNO")
        
        try:
            # Listar alunos
            alunos = self.repository.listar_todos()
            if not alunos:
                print("📭 Nenhum aluno cadastrado!")
                return
            
            print("📋 Alunos disponíveis:")
            for aluno in alunos:
                print(f"  {aluno.id} - {aluno.nome}")
            
            aluno_id_str = input("\nDigite o ID do aluno para remover: ").strip()
            if not aluno_id_str:
                print("❌ ID é obrigatório!")
                return
            
            aluno_id = int(aluno_id_str)
            aluno = self.repository.buscar_por_id(aluno_id)
            
            if not aluno:
                print(f"❌ Aluno com ID {aluno_id} não encontrado!")
                return
            
            confirmacao = input(f"\n⚠️ Tem certeza que deseja remover '{aluno.nome}'? (s/n): ").strip().lower()
            
            if confirmacao == 's':
                if self.repository.remover(aluno_id):
                    print(f"✅ Aluno '{aluno.nome}' removido com sucesso!")
                else:
                    print("❌ Erro ao remover aluno!")
            else:
                print("❌ Operação cancelada.")
        
        except ValueError as e:
            print(f"❌ Erro: {e}")
        except Exception as e:
            print(f"❌ Erro inesperado: {e}")
    
    def _mostrar_estatisticas(self):
        """Mostra estatísticas do sistema"""
        self.menu.exibir_cabecalho("📊 ESTATÍSTICAS DO SISTEMA")
        
        try:
            stats = self.repository.obter_estatisticas()
            self.menu.exibir_estatisticas(stats)
        except Exception as e:
            print(f"❌ Erro: {e}")


def main():
    """Função principal para executar o sistema"""
    sistema = SistemaAlunos()
    sistema.iniciar()


if __name__ == "__main__":
    main()
