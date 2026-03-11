import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Análise de Preferências Esportivas - Educação Física")

menu = st.sidebar.selectbox(
    "Selecione o Menu:",
    [
        "Esportes Preferidos",
        "Esportes Rejeitados",
        "Melhor Experiência",
        "Percepção da Disciplina"
    ]
)

# ============================
# CORES DOS CURSOS
# ============================

cores = {
    "adm": "#1f77b4",
    "info": "#ff7f0e",
    "agro": "#2ca02c",
    "zoo": "#d62728",
    "alt": "#9467bd"
}

# ============================
# CARREGAR DADOS AUTOMATICAMENTE
# ============================

df = pd.read_csv("data/dados_consolidados.csv")

# ============================
# FILTRO POR ANO
# ============================

anos_selecionados = st.sidebar.multiselect(
    "Selecione o ano",
    sorted(df["ano"].unique()),
    default=sorted(df["ano"].unique())
)

df = df[df["ano"].isin(anos_selecionados)]

# criar turma
df["turma"] = df["ano"].astype(str) + "º " + df["curso"]

turmas = sorted(df["turma"].unique())

turmas_selecionadas = st.sidebar.multiselect(
    "Selecione as turmas para comparar",
    turmas,
    default=turmas
)

top_x = st.sidebar.slider(
    "Quantidade de resultados exibidos (Top X)",
    min_value=3,
    max_value=20,
    value=10
)

tamanho_fonte = st.sidebar.slider(
    "Tamanho da fonte",
    min_value=12,
    max_value=40,
    value=20
)

# ============================
# GERAR GRÁFICOS
# ============================

if turmas_selecionadas:

    colunas_layout = st.columns(len(turmas_selecionadas))

    for i, turma in enumerate(turmas_selecionadas):

        df_turma = df[df["turma"] == turma]

        curso = df_turma["curso"].iloc[0].lower()

        with colunas_layout[i]:

            if menu == "Esportes Preferidos":

                dados = (
                    df_turma["ESPORTE +"]
                    .value_counts()
                    .head(top_x)
                    .reset_index()
                )

                dados.columns = ["Item", "Quantidade"]

                titulo = f"{turma}"

            elif menu == "Esportes Rejeitados":

                dados = (
                    df_turma["ESPORTE -"]
                    .value_counts()
                    .head(top_x)
                    .reset_index()
                )

                dados.columns = ["Item", "Quantidade"]

                titulo = f"{turma}"

            elif menu == "Melhor Experiência":

                dados = (
                    df_turma["MELHOR EXPERIÊNCIA"]
                    .value_counts()
                    .head(top_x)
                    .reset_index()
                )

                dados.columns = ["Item", "Quantidade"]

                titulo = f"{turma}"

            else:

                dados = (
                    df_turma["UMA PALAVRA"]
                    .value_counts()
                    .head(top_x)
                    .reset_index()
                )

                dados.columns = ["Item", "Quantidade"]

                titulo = f"{turma}"

            fig = px.bar(
                dados,
                x="Item",
                y="Quantidade",
                text="Quantidade",
                title=titulo,
                color_discrete_sequence=[cores.get(curso, "#333333")]
            )

            fig.update_traces(
                textposition="outside"
            )

            fig.update_layout(
                font=dict(size=tamanho_fonte),
                height=750,
                xaxis_title="",
                yaxis_title="Quantidade",
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Selecione pelo menos uma turma.")