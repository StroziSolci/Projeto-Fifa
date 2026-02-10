import streamlit as st
import requests
import base64


# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    layout="wide",
    page_title="Teams",
    page_icon="⚽"
)


# ===============================
# FUNÇÕES DE IMAGEM (ROBUSTAS)
# ===============================
@st.cache_data
def load_image_64(url):
    """
    Baixa uma imagem usando User-Agent de navegador
    e converte para base64.
    Se falhar (404, timeout, etc), retorna None.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return None

        return (
            "data:image/png;base64,"
            + base64.b64encode(response.content).decode()
        )

    except Exception:
        return None


def preprocess_row(value):
    """
    Converte URLs de imagem para base64.
    Qualquer coisa inválida vira None.
    """
    if isinstance(value, str) and value.startswith("http"):
        return load_image_64(value)
    return None


# ===============================
# GARANTIA DE SESSION STATE
# ===============================
if "data" not in st.session_state:
    st.error("Os dados não foram carregados. Volte para a página inicial.")
    st.stop()

df_data = st.session_state["data"]


# ===============================
# FILTRO DE CLUBES
# ===============================
clubes = df_data["Club"].value_counts().index
club = st.sidebar.selectbox("Clube", clubes)

df_filtered = (
    df_data[df_data["Club"] == club]
    .set_index("Name")
    .copy()
)


# ===============================
# TRATAMENTO EM MASSA DAS IMAGENS
# ===============================
df_filtered["Photo"] = df_filtered["Photo"].apply(preprocess_row)
df_filtered["Flag"] = df_filtered["Flag"].apply(preprocess_row)
df_filtered["Club Logo"] = df_filtered["Club Logo"].apply(preprocess_row)


# ===============================
# CABEÇALHO DO CLUBE
# ===============================
st.image(df_filtered.iloc[0]["Club Logo"])
st.markdown(f"## {club}")


# ===============================
# COLUNAS DA TABELA
# ===============================
columns = [
    "Age",
    "Photo",
    "Flag",
    "Overall",
    "Value(£)",
    "Wage(£)",
    "Joined",
    "Height(cm.)",
    "Weight(lbs.)",
    "Contract Valid Until",
    "Release Clause(£)"
]


# ===============================
# TABELA FINAL
# ===============================
st.dataframe(
    df_filtered[columns],
    column_config={
        "Overall": st.column_config.ProgressColumn(
            "Overall",
            min_value=0,
            max_value=100,
            format="%d"
        ),

        "Wage(£)": st.column_config.ProgressColumn(
            "Weekly Wage (£)",
            min_value=0,
            max_value=int(df_filtered["Wage(£)"].max()),
            format="£%d"
        ),

        "Photo": st.column_config.ImageColumn("Photo"),
        "Flag": st.column_config.ImageColumn("Flag"),
    },
    use_container_width=True
)
