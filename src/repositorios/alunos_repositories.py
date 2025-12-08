from pathlib import Path
from enum import Enum
import pandas as pd

from src.models.aluno_models import Aluno, Endereco, Contato

class Coluna(Enum):
    MATRICULA = "Matrícula"
    NOME = "Nome"
    RUA = "Rua"
    NUMERO = "Número"
    BAIRRO = "Bairro"
    CIDADE = "Cidade"
    UF = "UF"
    TELEFONE = "Telefone"
    EMAIL = "Email"

COLUNAS_CSV = [c.value for c in Coluna]

def obter_valor_coluna(linha, coluna):
    return str(linha[coluna.value])

def _csv_path():
    return Path(__file__).resolve().parents[2] / "alunos.csv"

def carregar_alunos():
    path = _csv_path()
    if not path.exists():
        return []

    df = pd.read_csv(path, dtype=str)
    
    for col in COLUNAS_CSV:
        if col not in df.columns:
            df[col] = ""
            
    df = df[COLUNAS_CSV].fillna("")

    alunos = []
    
    for _, linha in df.iterrows():
        endereco = Endereco(
            rua=obter_valor_coluna(linha, Coluna.RUA),
            numero=obter_valor_coluna(linha, Coluna.NUMERO),
            bairro=obter_valor_coluna(linha, Coluna.BAIRRO),
            cidade=obter_valor_coluna(linha, Coluna.CIDADE),
            uf=obter_valor_coluna(linha, Coluna.UF).upper(),
        )
        
        contato = Contato(
            telefone=obter_valor_coluna(linha, Coluna.TELEFONE),
            email=obter_valor_coluna(linha, Coluna.EMAIL),
        )
        
        aluno = Aluno(
            matricula=obter_valor_coluna(linha, Coluna.MATRICULA),
            nome=obter_valor_coluna(linha, Coluna.NOME),
            endereco=endereco,
            contato=contato,
        )
        
        alunos.append(aluno)
        
    return alunos

def salvar_dados(alunos):
    registros = [
        {
            Coluna.MATRICULA.value: str(aluno.matricula),
            Coluna.NOME.value: aluno.nome,
            Coluna.RUA.value: aluno.endereco.rua,
            Coluna.NUMERO.value: aluno.endereco.numero,
            Coluna.BAIRRO.value: aluno.endereco.bairro,
            Coluna.CIDADE.value: aluno.endereco.cidade,
            Coluna.UF.value: aluno.endereco.uf,
            Coluna.TELEFONE.value: aluno.contato.telefone,
            Coluna.EMAIL.value: aluno.contato.email,
        }
        for aluno in alunos
    ]

    df = pd.DataFrame(registros, columns=COLUNAS_CSV)
    df = df.astype(str)
    df.to_csv(_csv_path(), index=False)
