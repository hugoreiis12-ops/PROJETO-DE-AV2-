# src/alunos.py
import os
import pandas as pd

# Caminho do arquivo CSV
BASE_DIR = os.path.dirname(__file__)
CSV_PATH = os.path.join(BASE_DIR, "alunos.csv")

COLUMNS = [
    "Matrícula",
    "Nome",
    "Rua",
    "Número",
    "Bairro",
    "Cidade",
    "UF",
    "Telefone",
    "Email",
]


def criar_dataframe_base():
    """
    Lê o CSV se existir e retorna DataFrame correto.
    Caso não exista, retorna DataFrame vazio com colunas definidas.
    """
    if os.path.exists(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH, dtype=str)

            for col in COLUMNS:
                if col not in df.columns:
                    df[col] = ""

            df["Matrícula"] = df["Matrícula"].astype(str)
            df = df[COLUMNS]
            return df.reset_index(drop=True)

        except Exception:
            return pd.DataFrame(columns=COLUMNS)

    return pd.DataFrame(columns=COLUMNS)


def carregar_dados():
    """
    Apenas retorna o dataframe base.
    """
    return criar_dataframe_base()


def salvar_dados(df):
    """
    Salva dataframe no CSV com colunas em ordem.
    """
    df2 = df.copy()

    for col in COLUMNS:
        if col not in df2.columns:
            df2[col] = ""

    df2 = df2[COLUMNS]
    df2.to_csv(CSV_PATH, index=False)


def gerar_matricula(df):
    """
    Gera a próxima matrícula sequencial começando em 1001.
    """
    if df is None or df.empty:
        return 1001

    try:
        values = df["Matrícula"].dropna().astype(str)
        nums = []

        for m in values:
            if m.strip().isdigit():
                nums.append(int(m))

        if not nums:
            return 1001

        return max(nums) + 1

    except Exception:
        return 1001


def inserir_aluno_dict(df, aluno_dict):
    """
    Insere um novo aluno (dict) no dataframe e salva.
    """
    if df is None:
        df = criar_dataframe_base()

    df = df.copy()
    matricula = gerar_matricula(df)

    novo = {col: "" for col in COLUMNS}
    novo["Matrícula"] = str(matricula)

    for k, v in aluno_dict.items():
        if k in novo:
            novo[k] = str(v).strip()
        else:
            kk = k.lower()
            if kk in ("numero", "número"):
                novo["Número"] = v
            elif kk == "bairro":
                novo["Bairro"] = v
            elif kk == "cidade":
                novo["Cidade"] = v
            elif kk == "uf":
                novo["UF"] = v
            elif kk in ("telefone", "tel"):
                novo["Telefone"] = v
            elif kk in ("email", "e-mail"):
                novo["Email"] = v
            elif kk == "nome":
                novo["Nome"] = v
            elif kk == "rua":
                novo["Rua"] = v

    # append substituído por concat (append foi removido do pandas)
    df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)

    salvar_dados(df)
    return df


def pesquisar(df, termo):
    """
    Pesquisa aluno por matrícula ou nome (case-insensitive).
    """
    if df is None:
        return pd.DataFrame(columns=COLUMNS)

    df = df.copy()
    termo = str(termo).strip()

    if termo == "":
        return pd.DataFrame(columns=COLUMNS)

    if termo.isdigit():
        result = df[df["Matrícula"].astype(str) == termo]
        return result.reset_index(drop=True)

    mask = df["Nome"].astype(str).str.lower().str.contains(termo.lower())
    return df[mask].reset_index(drop=True)


def editar_aluno(df, matricula, dados):
    """
    Edita um aluno existente.
    """
    if df is None:
        return pd.DataFrame(columns=COLUMNS)

    df = df.copy()
    matricula = str(matricula).strip()

    idx = df.index[df["Matrícula"].astype(str) == matricula].tolist()

    if not idx:
        return df

    i = idx[0]

    for k, v in dados.items():
        if k == "Matrícula":
            continue

        if k in COLUMNS:
            df.at[i, k] = str(v).strip()
        else:
            kk = k.lower()
            if kk in ("numero", "número"):
                df.at[i, "Número"] = v
            elif kk == "bairro":
                df.at[i, "Bairro"] = v
            elif kk == "cidade":
                df.at[i, "Cidade"] = v
            elif kk == "uf":
                df.at[i, "UF"] = v
            elif kk in ("telefone", "tel"):
                df.at[i, "Telefone"] = v
            elif kk in ("email", "e-mail"):
                df.at[i, "Email"] = v
            elif kk == "nome":
                df.at[i, "Nome"] = v
            elif kk == "rua":
                df.at[i, "Rua"] = v

    salvar_dados(df)
    return df


def remover_aluno(df, matricula):
    """
    Remove o aluno com a matrícula informada.
    """
    if df is None:
        return pd.DataFrame(columns=COLUMNS)

    df = df.copy()
    matricula = str(matricula).strip()

    df2 = df[df["Matrícula"].astype(str) != matricula].reset_index(drop=True)

    salvar_dados(df2)
    return df2
