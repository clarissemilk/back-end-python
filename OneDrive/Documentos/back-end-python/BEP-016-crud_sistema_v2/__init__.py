"""
Sistema CRUD de Gerenciamento de Alunos - Versão 2 (Orientada a Objetos - Simplificada)
Módulo organizado usando Programação Orientada a Objetos básica
Demonstra conceitos básicos de: Classes, Encapsulamento, Composição, Tratamento de Exceções
"""

__version__ = "2.0.0-simplificado"
__author__ = "BEP-016 - Versão OO Simplificada"

# Importações principais para facilitar uso
from .models import Aluno
from .database import DatabaseManager
from .repository import AlunoRepository
from .menu import Menu
from .sistema import SistemaAlunos
from .exceptions import ErroSistema

__all__ = [
    'Aluno',
    'DatabaseManager',
    'AlunoRepository',
    'Menu',
    'SistemaAlunos',
    'ErroSistema'
]
