from src.models.aluno_models import Aluno, Endereco, Contato
from datetime import datetime

def gerar_matricula():
    """Gera uma nova matrícula baseada no timestamp."""
    return str(int(datetime.now().timestamp()))

def inserir(alunos, dados):
    """Insere um novo aluno na lista."""
    # Validar dados obrigatórios
    if not dados.get("Nome", "").strip():
        raise ValueError("Nome é obrigatório.")
    
    # Criar novo aluno
    endereco = Endereco(
        rua=dados.get("Rua", "").strip(),
        numero=dados.get("Número", "").strip(),
        bairro=dados.get("Bairro", "").strip(),
        cidade=dados.get("Cidade", "").strip(),
        uf=dados.get("UF", "").strip().upper(),
    )
    
    contato = Contato(
        telefone=dados.get("Telefone", "").strip(),
        email=dados.get("Email", "").strip(),
    )
    
    novo_aluno = Aluno(
        matricula=gerar_matricula(),
        nome=dados.get("Nome", "").strip(),
        endereco=endereco,
        contato=contato,
    )
    
    alunos.append(novo_aluno)
    return alunos, novo_aluno

def pesquisar_por_termo(alunos, termo):
    """Pesquisa alunos por matrícula ou nome."""
    termo = termo.lower().strip()
    resultados = []
    
    for aluno in alunos:
        if termo in aluno.matricula or termo in aluno.nome.lower():
            resultados.append(aluno)
    
    return resultados

def campos_editaveis():
    """Retorna lista de campos que podem ser editados."""
    return ["Nome", "Rua", "Número", "Bairro", "Cidade", "UF", "Telefone", "Email"]

def editar_campo(aluno, campo, novo_valor):
    """Edita um campo específico do aluno."""
    novo_valor = novo_valor.strip()
    
    if campo == "Nome":
        if not novo_valor:
            raise ValueError("Nome não pode ser vazio.")
        aluno.nome = novo_valor
    elif campo == "Rua":
        aluno.endereco.rua = novo_valor
    elif campo == "Número":
        aluno.endereco.numero = novo_valor
    elif campo == "Bairro":
        aluno.endereco.bairro = novo_valor
    elif campo == "Cidade":
        aluno.endereco.cidade = novo_valor
    elif campo == "UF":
        aluno.endereco.uf = novo_valor.upper()
    elif campo == "Telefone":
        aluno.contato.telefone = novo_valor
    elif campo == "Email":
        aluno.contato.email = novo_valor
    else:
        raise ValueError(f"Campo '{campo}' inválido.")

def remover_por_matricula(alunos, matricula):
    """Remove um aluno da lista pela matrícula."""
    return [a for a in alunos if a.matricula != matricula]

def formatar_aluno(aluno):
    """Formata os dados do aluno para exibição."""
    linhas = [
        "",
        "=== DADOS DO ALUNO ===",
        f"Matrícula: {aluno.matricula}",
        f"Nome: {aluno.nome}",
        "--- ENDEREÇO ---",
        f"Rua: {aluno.endereco.rua}",
        f"Número: {aluno.endereco.numero}",
        f"Bairro: {aluno.endereco.bairro}",
        f"Cidade: {aluno.endereco.cidade}",
        f"UF: {aluno.endereco.uf}",
        "--- CONTATO ---",
        f"Telefone: {aluno.contato.telefone}",
        f"Email: {aluno.contato.email}",
        "",
    ]
    return linhas
