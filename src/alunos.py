import os
import pandas as pd
import unicodedata

# Caminho de arquivo CSV (mesma pasta do módulo)
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


def normalizar(texto):
    """
    Remove acentos e coloca tudo em minúsculo para permitir busca inteligente.
    """
    if texto is None:
        return ""
    texto = str(texto)
    texto = unicodedata.normalize("NFD", texto)
    texto = texto.encode("ascii", "ignore").decode("utf-8")
    return texto.lower()


def criar_dataframe_base():
    """
    Lê o CSV se existir e retorna DataFrame com colunas corretas.
    Caso não exista, retorna df vazio com colunas definidas.
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
    else:
        return pd.DataFrame(columns=COLUMNS)


def salvar_dataframe(df):
    """
    Salvar o dataframe em CSV.
    """
    df_to_save = df.copy()
    for col in COLUMNS:
        if col not in df_to_save.columns:
            df_to_save[col] = ""
    df_to_save = df_to_save[COLUMNS]
    df_to_save.to_csv(CSV_PATH, index=False)


def gerar_matricula(df):
    """
    Gerar próxima matrícula sequencial começando em 1001.
    """
    if df is None or df.empty:
        return 1001

    try:
        mats = df["Matrícula"].dropna().astype(str)
        nums = []

        for m in mats:
            m_strip = m.strip()
            if m_strip.isdigit():
                nums.append(int(m_strip))

        if not nums:
            return 1001

        return max(nums) + 1
    except Exception:
        return 1001


def inserir_aluno_dict(df, aluno_dict):
    """
    Inserir aluno com matrícula manual (se enviada) ou automática.
    """
    if df is None:
        df = criar_dataframe_base()

    df = df.copy()

    # matrícula manual
    if "Matrícula" in aluno_dict and aluno_dict["Matrícula"].strip() != "":
        matricula = aluno_dict["Matrícula"].strip()

        # checar duplicação
        existente = df[df["Matrícula"].astype(str) == matricula]
        if not existente.empty:
            raise ValueError(f"Já existe um aluno com a matrícula {matricula}.")
    else:
        matricula = str(gerar_matricula(df))

    novo = {col: "" for col in COLUMNS}
    novo["Matrícula"] = matricula

    for k, v in aluno_dict.items():
        if k in novo:
            novo[k] = str(v).strip()

    df = df.append(novo, ignore_index=True)
    salvar_dataframe(df)
    return df


def pesquisar(df, termo):
    """
    Pesquisa por matrícula ou nome (case-insensitive, sem acentos).
    """
    if df is None:
        return pd.DataFrame(columns=COLUMNS)

    df = df.copy()
    termo = str(termo).strip()

    if termo == "":
        return pd.DataFrame(columns=COLUMNS)

    # Caso matrícula (somente números)
    if termo.isdigit():
        res = df[df["Matrícula"].astype(str) == termo]
        return res.reset_index(drop=True)

    # Caso nome → normalizar
    termo_norm = normalizar(termo)

    df["Nome_norm"] = df["Nome"].apply(normalizar)

    mask = df["Nome_norm"].str.contains(termo_norm, na=False)
    resultados = df[mask].drop(columns=["Nome_norm"])

    return resultados.reset_index(drop=True)


def editar_aluno(df, matricula, dados_atualizados: dict):
    """
    Edita aluno pela matrícula.
    """
    if df is None:
        return pd.DataFrame(columns=COLUMNS)

    df = df.copy()
    matricula_str = str(matricula).strip()

    idx = df.index[df["Matrícula"].astype(str) == matricula_str].tolist()

    if not idx:
        return df

    i = idx[0]

    for k, v in dados_atualizados.items():
        if k == "Matrícula":
            continue

        if k in COLUMNS:
            df.at[i, k] = str(v).strip()
        else:
            # mapeamentos simples
            if k.lower() in ("numero", "número"):
                df.at[i, "Número"] = str(v).strip()
            elif k.lower() == "bairro":
                df.at[i, "Bairro"] = str(v).strip()
            elif k.lower() == "cidade":
                df.at[i, "Cidade"] = str(v).strip()
            elif k.lower() == "uf":
                df.at[i, "UF"] = str(v).strip()
            elif k.lower() in ("telefone", "tel"):
                df.at[i, "Telefone"] = str(v).strip()
            elif k.lower() in ("email", "e-mail"):
                df.at[i, "Email"] = str(v).strip()
            elif k.lower() == "nome":
                df.at[i, "Nome"] = str(v).strip()
            elif k.lower() == "rua":
                df.at[i, "Rua"] = str(v).strip()

    salvar_dataframe(df)
    return df


def remover_aluno(df, matricula):
    """
    Remove aluno pela matrícula.
    """
    if df is None:
        return pd.DataFrame(columns=COLUMNS)

    df = df.copy()
    matricula_str = str(matricula).strip()

    df_new = df[df["Matrícula"].astype(str) != matricula_str].reset_index(drop=True)
    salvar_dataframe(df_new)
    return df_new
