# main py
from src.repositorios.alunos_repositories import carregar_alunos, salvar_dados
from src.services.alunos_services import (
    inserir,
    pesquisar_por_termo,
    campos_editaveis,
    editar_campo,
    remover_por_matricula,
    formatar_aluno,
)
from enum import Enum

class OpcaoMenu(Enum):
    INSERIR = "1"
    PESQUISAR = "2"
    SAIR = "3"

def solicitar_entrada(mensagem):
    return input(mensagem)

def exibir_menu_principal():
    print("\n=== TRABALHO PRÁTICO AV2 - MENU ===")
    print("1 - INSERIR")
    print("2 - PESQUISAR")
    print("3 - SAIR")
    entrada = solicitar_entrada("Escolha uma opção: ").strip()
    mapa = {
        "1": OpcaoMenu.INSERIR,
        "2": OpcaoMenu.PESQUISAR,
        "3": OpcaoMenu.SAIR,
    }
    return mapa.get(entrada)

def processar_insercao(alunos):
    print("\n== Inserir Aluno ==")
    dados = {
        "Nome": solicitar_entrada("Nome: ").strip(),
        "Rua": solicitar_entrada("Rua: ").strip(),
        "Número": solicitar_entrada("Número: ").strip(),
        "Bairro": solicitar_entrada("Bairro: ").strip(),
        "Cidade": solicitar_entrada("Cidade: ").strip(),
        "UF": solicitar_entrada("UF (2 letras): ").strip(),
        "Telefone": solicitar_entrada("Telefone: ").strip(),
        "Email": solicitar_entrada("Email: ").strip(),
    }
    try:
        alunos, novo = inserir(alunos, dados)
        salvar_dados(alunos)
        print(f"Aluno cadastrado com matrícula {novo.matricula}.")
    except ValueError as e:
        print(f"Erro: {e}")
    return alunos

def processar_pesquisa(alunos):
    print("\n== Pesquisar Aluno ==")
    
    if not alunos:
        print("Nenhum aluno cadastrado.")
        return None
    
    termo = solicitar_entrada("Termo de pesquisa (matrícula ou nome): ").strip()
    resultados = pesquisar_por_termo(alunos, termo)
    
    if not resultados:
        print("Aluno não encontrado.")
        return None
    
    if len(resultados) == 1:
        return resultados[0]
    
    if len(resultados) > 1:
        print("Foram encontrados múltiplos alunos:")
        for a in resultados:
            print(f"Matrícula {a.matricula} - {a.nome}")
            
    sel = solicitar_entrada("Digite a matrícula para selecionar (ou ENTER p/ cancelar): ").strip()
    
    if sel == "":
        print("Operação cancelada.")
        return None
    
    selecionados = [a for a in resultados if a.matricula == sel]
    
    if not selecionados:
        print("Matrícula inválida.")
        return None
    
    return selecionados[0]

def processar_edicao(alunos, aluno):
    for linha in formatar_aluno(aluno):
        print(linha)
    
    acao = exibir_menu_acao()
    
    if acao == "1":
        return editar_dados_aluno(alunos, aluno)
    elif acao == "2":
        return remover_aluno(alunos, aluno)
    elif acao == "3" or acao == "":
        print("Operação cancelada.")
        return alunos
    else:
        print("Opção inválida.")
        return alunos

def exibir_menu_acao():
    print("\nO que deseja fazer?")
    print("1 - Editar")
    print("2 - Remover")
    print("3 - Voltar")
    
    return solicitar_entrada("Escolha uma opção: ").strip()

def exibir_dados_aluno(aluno):
    for linha in formatar_aluno(aluno):
        print(linha)

def editar_dados_aluno(alunos, aluno):
    opcoes = campos_editaveis()
    
    print("\nQual campo deseja editar?")
    
    for i, c in enumerate(opcoes, start=1):
        print(f"{i} - {c}")
        
    esc = solicitar_entrada("Informe a opção: ").strip()
    
    if not esc.isdigit() or not (1 <= int(esc) <= len(opcoes)):
        print("Opção inválida.")
        return alunos
    
    campo = opcoes[int(esc) - 1]
    novo_valor = solicitar_entrada(f"Novo valor para {campo}: ").strip()
    
    try:
        editar_campo(aluno, campo, novo_valor)
        salvar_dados(alunos)
        
        print("Dados do aluno atualizados.")
        
        exibir_dados_aluno(aluno)
    except ValueError as e:
        print(f"Erro: {e}")
        
    return alunos

def remover_aluno(alunos, aluno):
    conf = solicitar_entrada("Confirmar remoção? (S/N): ").strip().upper()
    
    if conf == "S":
        alunos = remover_por_matricula(alunos, aluno.matricula)
        salvar_dados(alunos)
        print("Aluno removido.")
    else:
        print("Remoção cancelada.")
    return alunos

def processar_pesquisa_opcao(alunos):
    selecionado = processar_pesquisa(alunos)
    
    if selecionado:
        return processar_edicao(alunos, selecionado)
    
    return alunos

def processar_saida():
    print("Saindo... Até mais.")

def main():
    alunos = carregar_alunos()
    
    while True:
        opcao = exibir_menu_principal()
        
        match opcao:
            case OpcaoMenu.INSERIR:
                alunos = processar_insercao(alunos)
            case OpcaoMenu.PESQUISAR:
                alunos = processar_pesquisa_opcao(alunos)
            case OpcaoMenu.SAIR:
                processar_saida()
                break
            case None:
                print("Opção inválida.")

if __name__ == "__main__":
    main()
