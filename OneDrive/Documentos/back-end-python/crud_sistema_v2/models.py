"""
Módulo de Modelos (Entidades)
Aplica conceitos básicos de BEP-017, BEP-019: Classes, Encapsulamento com @property
Seguindo o padrão básico ensinado na BEP-019
"""


class Aluno:
    """
    Classe que representa um Aluno
    Versão simplificada - usando @property (forma pythônica)
    """
    
    def __init__(self, nome, idade=None, curso=None, nota=None, aluno_id=None, data_cadastro=None):
        """
        Construtor da classe Aluno
        
        Args:
            nome: Nome completo do aluno (obrigatório)
            idade: Idade do aluno (opcional)
            curso: Curso do aluno (opcional)
            nota: Nota do aluno entre 0 e 10 (opcional)
            aluno_id: ID do aluno no banco (gerado automaticamente)
            data_cadastro: Data de cadastro (gerada automaticamente)
        """
        # Atributos que não precisam de validação especial
        self._id = aluno_id
        self._curso = curso
        self._data_cadastro = data_cadastro
        self._idade = idade
        
        # Atributos com validação: inicializar privado e usar setter
        # Padrão da BEP-019: self.__atributo = valor_inicial, depois self.atributo = valor
        self.__nome = ""  # Inicializa vazio
        self.nome = nome  # Usa o setter para validar
        
        self.__nota = 0  # Inicializa
        if nota is not None:
            self.nota = nota  # Usa o setter para validar
        else:
            self.__nota = None
    
    # Getters com @property (forma pythônica)
    @property
    def id(self):
        """Retorna o ID do aluno"""
        return self._id
    
    @property
    def nome(self):
        """Retorna o nome do aluno"""
        return self.__nome
    
    @property
    def idade(self):
        """Retorna a idade do aluno"""
        return self._idade
    
    @property
    def curso(self):
        """Retorna o curso do aluno"""
        return self._curso
    
    @property
    def nota(self):
        """Retorna a nota do aluno"""
        return self.__nota
    
    @property
    def data_cadastro(self):
        """Retorna a data de cadastro"""
        return self._data_cadastro
    
    # Setters com validação (forma pythônica)
    @nome.setter
    def nome(self, valor):
        """Define o nome do aluno com validação"""
        if not valor or not valor.strip():
            raise ValueError("Nome é obrigatório e não pode estar vazio")
        self.__nome = valor
    
    @nota.setter
    def nota(self, valor):
        """Define a nota do aluno com validação"""
        if valor is not None and (valor < 0 or valor > 10):
            raise ValueError("Nota deve estar entre 0 e 10")
        self.__nota = valor
    
    def atualizar(self, nome=None, idade=None, curso=None, nota=None):
        """
        Atualiza os dados do aluno
        
        Args:
            nome: Novo nome (opcional)
            idade: Nova idade (opcional)
            curso: Novo curso (opcional)
            nota: Nova nota (opcional)
        """
        if nome is not None:
            self.nome = nome  # Usa o setter com validação
        
        if idade is not None:
            self._idade = idade  # Atributo sem validação especial
        
        if curso is not None:
            self._curso = curso  # Atributo sem validação especial
        
        if nota is not None:
            self.nota = nota  # Usa o setter com validação
    
    def __str__(self):
        """Representação em string do aluno"""
        idade_str = str(self._idade) if self._idade else "N/A"
        curso_str = self._curso if self._curso else "N/A"
        nota_str = f"{self.__nota:.1f}" if self.__nota else "N/A"
        
        return (f"Aluno(id={self._id}, nome='{self.__nome}', "
                f"idade={idade_str}, curso='{curso_str}', nota={nota_str})")
