import streamlit as st
import requests
import base64


# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    layout="wide",
    page_title="Players",
    page_icon="🏃‍♂️"
)


# ===============================
# FUNÇÃO DE IMAGEM ROBUSTA
# ===============================
@st.cache_data
def load_image_64(url):
    """
    Baixa a imagem com User-Agent de navegador
    e converte para base64.
    Se falhar, retorna None.
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


# ===============================
# GARANTIA DE SESSION STATE
# ===============================
if "data" not in st.session_state:
    st.error("Os dados não foram carregados. Volte para a página inicial.")
    st.stop()

df_data = st.session_state["data"]


# ===============================
# FILTROS (CLUBE → JOGADOR)
# ===============================
clubes = df_data["Club"].value_counts().index
clube = st.sidebar.selectbox("Clube", clubes)

df_players = df_data[df_data["Club"] == clube]

players = df_players["Name"].value_counts().index
player = st.sidebar.selectbox("Jogador", players)

player_stats = df_players[df_players["Name"] == player].iloc[0]


# ===============================
# CABEÇALHO DO JOGADOR
# ===============================
photo = load_image_64(player_stats["Photo"])

if photo:
    st.image(photo)

st.title(player_stats["Name"])

st.markdown(f"**Clube:** {player_stats['Club']}")
st.markdown(f"**Posição:** {player_stats['Position']}")


# ===============================
# DADOS FÍSICOS
# ===============================
col1, col2, col3, col4 = st.columns(4)

col1.markdown(f"**Idade:** {player_stats['Age']}")
col2.markdown(f"**Altura:** {player_stats['Height(cm.)'] / 100:.2f} m")
col3.markdown(f"**Peso:** {player_stats['Weight(lbs.)'] * 0.453:.2f} kg")


# ===============================
# OVERALL
# ===============================
st.divider()

st.subheader(f"Overall — {player_stats['Overall']}")
st.progress(int(player_stats["Overall"]))


# ===============================
# VALORES FINANCEIROS
# ===============================
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Valor de mercado",
    value=f"£ {player_stats['Value(£)']:,}"
)

col2.metric(
    label="Remuneração semanal",
    value=f"£ {player_stats['Wage(£)']:,}"
)

col3.metric(
    label="Cláusula de rescisão",
    value=f"£ {player_stats['Release Clause(£)']:,}"
)
