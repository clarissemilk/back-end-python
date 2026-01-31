"""
Módulo de Repositório (Operações CRUD)
Aplica conceitos básicos de BEP-017, BEP-021: Classes, Composição simples
"""

from .models import Aluno
from .database import DatabaseManager


class AlunoRepository:
    """
    Classe responsável pelas operações CRUD no banco de dados
    Versão simplificada - apenas métodos de classe
    """
    
    def __init__(self, db_manager):
        """
        Inicializa o repositório com um gerenciador de banco
        
        Args:
            db_manager: Instância de DatabaseManager (Composição)
        """
        self.db_manager = db_manager
    
    def criar(self, aluno):
        """
        Cria um novo aluno no banco de dados
        
        Args:
            aluno: Objeto Aluno a ser criado
        
        Returns:
            Aluno criado com ID atribuído
        """
        try:
            cursor = self.db_manager.get_cursor()
            cursor.execute('''
                INSERT INTO alunos (nome, idade, curso, nota)
                VALUES (?, ?, ?, ?)
            ''', (aluno.nome, aluno.idade, aluno.curso, aluno.nota))
            
            self.db_manager.connection.commit()
            
            # Obter ID gerado
            aluno_id = cursor.lastrowid
            
            # Buscar aluno completo
            return self.buscar_por_id(aluno_id)
        except Exception as e:
            print(f"❌ Erro ao criar aluno: {e}")
            return None
    
    def buscar_por_id(self, aluno_id):
        """
        Busca um aluno pelo ID
        
        Args:
            aluno_id: ID do aluno
        
        Returns:
            Objeto Aluno encontrado ou None
        """
        try:
            cursor = self.db_manager.get_cursor()
            cursor.execute("SELECT * FROM alunos WHERE id = ?", (aluno_id,))
            resultado = cursor.fetchone()
            
            if not resultado:
                return None
            
            # Criar objeto Aluno a partir da tupla
            aluno_id_db, nome, idade, curso, nota, data_cadastro = resultado
            return Aluno(
                nome=nome,
                idade=idade,
                curso=curso,
                nota=nota,
                aluno_id=aluno_id_db,
                data_cadastro=data_cadastro
            )
        except Exception as e:
            print(f"❌ Erro ao buscar aluno: {e}")
            return None
    
    def buscar_por_nome(self, nome):
        """
        Busca alunos por nome (usando LIKE)
        
        Args:
            nome: Nome ou parte do nome para buscar
        
        Returns:
            Lista de alunos encontrados
        """
        try:
            cursor = self.db_manager.get_cursor()
            cursor.execute(
                "SELECT * FROM alunos WHERE nome LIKE ? ORDER BY nome",
                (f"%{nome}%",)
            )
            resultados = cursor.fetchall()
            
            alunos = []
            for row in resultados:
                aluno_id, nome_db, idade, curso, nota, data_cadastro = row
                aluno = Aluno(
                    nome=nome_db,
                    idade=idade,
                    curso=curso,
                    nota=nota,
                    aluno_id=aluno_id,
                    data_cadastro=data_cadastro
                )
                alunos.append(aluno)
            
            return alunos
        except Exception as e:
            print(f"❌ Erro ao buscar alunos: {e}")
            return []
    
    def listar_todos(self):
        """
        Lista todos os alunos cadastrados
        
        Returns:
            Lista de todos os alunos
        """
        try:
            cursor = self.db_manager.get_cursor()
            cursor.execute("SELECT * FROM alunos ORDER BY nome")
            resultados = cursor.fetchall()
            
            alunos = []
            for row in resultados:
                aluno_id, nome, idade, curso, nota, data_cadastro = row
                aluno = Aluno(
                    nome=nome,
                    idade=idade,
                    curso=curso,
                    nota=nota,
                    aluno_id=aluno_id,
                    data_cadastro=data_cadastro
                )
                alunos.append(aluno)
            
            return alunos
        except Exception as e:
            print(f"❌ Erro ao listar alunos: {e}")
            return []
    
    def atualizar(self, aluno):
        """
        Atualiza um aluno existente
        
        Args:
            aluno: Objeto Aluno com dados atualizados (deve ter ID)
        
        Returns:
            True se atualizado com sucesso, False caso contrário
        """
        if not aluno.id:
            print("❌ Aluno deve ter ID para ser atualizado")
            return False
        
        try:
            # Verificar se existe
            aluno_existente = self.buscar_por_id(aluno.id)
            if not aluno_existente:
                print(f"❌ Aluno com ID {aluno.id} não encontrado!")
                return False
            
            cursor = self.db_manager.get_cursor()
            cursor.execute('''
                UPDATE alunos 
                SET nome = ?, idade = ?, curso = ?, nota = ?
                WHERE id = ?
            ''', (aluno.nome, aluno.idade, aluno.curso, aluno.nota, aluno.id))
            
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print(f"❌ Erro ao atualizar aluno: {e}")
            return False
    
    def remover(self, aluno_id):
        """
        Remove um aluno do banco de dados
        
        Args:
            aluno_id: ID do aluno a ser removido
        
        Returns:
            True se removido com sucesso, False caso contrário
        """
        try:
            # Verificar se existe
            aluno = self.buscar_por_id(aluno_id)
            if not aluno:
                print(f"❌ Aluno com ID {aluno_id} não encontrado!")
                return False
            
            cursor = self.db_manager.get_cursor()
            cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))
            self.db_manager.connection.commit()
            return True
        except Exception as e:
            print(f"❌ Erro ao remover aluno: {e}")
            return False
    
    def contar_total(self):
        """
        Retorna o total de alunos cadastrados
        
        Returns:
            Número total de alunos
        """
        try:
            cursor = self.db_manager.get_cursor()
            cursor.execute("SELECT COUNT(*) FROM alunos")
            return cursor.fetchone()[0]
        except Exception as e:
            print(f"❌ Erro ao contar alunos: {e}")
            return 0
    
    def obter_estatisticas(self):
        """
        Obtém estatísticas do banco de dados
        
        Returns:
            Dicionário com estatísticas
        """
        try:
            stats = {}
            cursor = self.db_manager.get_cursor()
            
            # Total de alunos
            cursor.execute("SELECT COUNT(*) FROM alunos")
            stats['total'] = cursor.fetchone()[0]
            
            # Alunos por curso
            cursor.execute('''
                SELECT curso, COUNT(*) as quantidade 
                FROM alunos 
                WHERE curso IS NOT NULL AND curso != ''
                GROUP BY curso 
                ORDER BY quantidade DESC
            ''')
            stats['por_curso'] = dict(cursor.fetchall())
            
            # Média das notas
            cursor.execute("SELECT AVG(nota) FROM alunos WHERE nota IS NOT NULL")
            resultado = cursor.fetchone()[0]
            stats['media_notas'] = round(resultado, 2) if resultado else None
            
            # Cadastrados hoje
            cursor.execute("SELECT COUNT(*) FROM alunos WHERE data_cadastro = DATE('now')")
            stats['cadastrados_hoje'] = cursor.fetchone()[0]
            
            # Melhor nota
            cursor.execute("SELECT MAX(nota), nome FROM alunos WHERE nota IS NOT NULL")
            resultado = cursor.fetchone()
            if resultado[0]:
                stats['melhor_nota'] = {
                    'nota': round(resultado[0], 1),
                    'aluno': resultado[1]
                }
            else:
                stats['melhor_nota'] = None
            
            return stats
        except Exception as e:
            print(f"❌ Erro ao obter estatísticas: {e}")
            return {}
