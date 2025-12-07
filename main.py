# main.py
import os
import sys

# garantir que o src esteja no path se rodar a partir da raiz 
THIS_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(THIS_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from src.alunos import ( criar_dataframe_base,
    gerar_matricula,
    inserir_aluno_dict,
    pesquisar,
    editar_aluno,
    remover_aluno,
)

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")


def input_com_prompt(prompt):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        return ""


def mostrar_aluno(linha):
    """
    Linha é uma Series do DataFrame
    """
    print("-----")
    for col in linha.index:
        print(f"{col}: {linha[col]}")
    print("-----")


def inserir_fluxo(df):
    print("\n=== Inserir novo aluno ===")
    aluno = {}
    aluno["Nome"] = input_com_prompt("Nome: ").strip()
    aluno["Rua"] = input_com_prompt("Rua: ").strip()
    aluno["Número"] = input_com_prompt("Número: ").strip()
    aluno["Bairro"] = input_com_prompt("Bairro: ").strip()
    aluno["Cidade"] = input_com_prompt("Cidade: ").strip()
    aluno["UF"] = input_com_prompt("UF: ").strip().upper()
    aluno["Telefone"] = input_com_prompt("Telefone: ").strip()
    aluno["Email"] = input_com_prompt("Email: ").strip()
    df = inserir_aluno_dict(df, aluno)
    print(f"Aluno inserido com matrícula {gerar_matricula(df) - 1}")
    return df


def pesquisar_fluxo(df):
    print("\n=== Pesquisar aluno ===")
    termo = input_com_prompt("Digite matrícula ou nome: ").strip()
    if termo == "":
        print("Pesquisa vazia.")
        return df
    res = pesquisar(df, termo)
    if res.empty:
        print("Nenhum aluno encontrado.")
        return df
    # mostrar resultados
    print(f"\nForam encontrados {len(res)} resultado(s):")
    for i in range(len(res)):
        print(f"\nResultado #{i+1}:")
        mostrar_aluno(res.iloc[i])

    # se mais de um resultado, pedir qual matrícula operar (opcional)
    # Perguntar se deseja editar ou remover
    escolha = input_com_prompt("\nDeseja (E)ditar, (R)emover ou (V)oltar? [E/R/V]: ").strip().lower()
    if escolha == "e":
        matricula = input_com_prompt("Digite a matrícula do aluno a editar: ").strip()
        if matricula == "":
            print("Matrícula vazia. Abortando edição.")
            return df
        res_edit = pesquisar(df, matricula)
        if res_edit.empty:
            print("Matrícula não encontrada.")
            return df
        # mostrar dados atuais
        print("\nDados atuais:")
        mostrar_aluno(res_edit.iloc[0])
        # Perguntar qual campo editar
        campos = [c for c in res_edit.columns if c != "Matrícula"]
        print("\nCampos editáveis:")
        for idx, c in enumerate(campos, start=1):
            print(f"{idx} - {c}")
        try:
            opt = int(input_com_prompt("Escolha o número do campo a editar: ").strip())
            if opt < 1 or opt > len(campos):
                print("Opção inválida. Abortando edição.")
                return df
            campo_escolhido = campos[opt - 1]
            novo_valor = input_com_prompt(f"Novo valor para {campo_escolhido}: ").strip()
            if novo_valor == "":
                print("Valor vazio. Abortando edição.")
                return df
            df = editar_aluno(df, matricula, {campo_escolhido: novo_valor})
            print("Aluno atualizado com sucesso.")
        except ValueError:
            print("Entrada inválida. Abortando edição.")
        return df

    elif escolha == "r":
        matricula = input_com_prompt("Digite a matrícula do aluno a remover: ").strip()
        if matricula == "":
            print("Matrícula vazia. Abortando remoção.")
            return df
        res_rem = pesquisar(df, matricula)
        if res_rem.empty:
            print("Matrícula não encontrada.")
            return df
        # confirmação
        print("\nRegistro encontrado:")
        mostrar_aluno(res_rem.iloc[0])
        conf = input_com_prompt("Deseja realmente remover este aluno? (s/N): ").strip().lower()
        if conf == "s":
            df = remover_aluno(df, matricula)
            print("Aluno removido.")
        else:
            print("Remoção cancelada.")
        return df

    else:
        return df


def main():
    df = criar_dataframe_base()
    while True:
        print("\n=== TRABALHO PRÁTICO AV2 - MENU ===")
        print("1 - INSERIR")
        print("2 - PESQUISAR")
        print("3 - SAIR")
        escolha = input_com_prompt("Escolha uma opção: ").strip()
        if escolha == "1":
            df = inserir_fluxo(df)
        elif escolha == "2":
            df = pesquisar_fluxo(df)
        elif escolha == "3":
            print("Saindo... Até mais.")
            break
        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
