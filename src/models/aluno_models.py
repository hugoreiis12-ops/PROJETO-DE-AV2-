from dataclasses import dataclass

@dataclass
class Endereco:
    rua: str
    numero: str
    bairro: str
    cidade: str
    uf: str

@dataclass
class Contato:
    telefone: str
    email: str

@dataclass
class Aluno:
    matricula: str
    nome: str
    endereco: Endereco
    contato: Contato
