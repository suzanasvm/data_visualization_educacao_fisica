import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Painel de Preferências Esportivas dos Estudantes")

# carregar dados
df = pd.read_csv("data/dados_consolidados.csv")

st.sidebar.header("Filtros")

anos = st.sidebar.multiselect(
    "Selecione o ano",
    options=sorted(df["ano"].unique()),
    default=sorted(df["ano"].unique())
)

cursos = st.sidebar.multiselect(
    "Selecione o curso",
    options=sorted(df["curso"].unique()),
    default=sorted(df["curso"].unique())
)

df_filtrado = df[(df["ano"].isin(anos)) & (df["curso"].isin(cursos))]

st.write("Total de estudantes analisados:", len(df_filtrado))

col1, col2 = st.columns(2)

with col1:

    st.subheader("Esportes Preferidos")

    pref = (
        df_filtrado["ESPORTE +"]
        .value_counts()
        .reset_index()
    )

    pref.columns = ["esporte", "quantidade"]

    fig = px.bar(
        pref,
        x="esporte",
        y="quantidade",
        title="Esportes mais preferidos"
    )

    st.plotly_chart(fig, use_container_width=True)


with col2:

    st.subheader("Esportes Menos Preferidos")

    neg = (
        df_filtrado["ESPORTE -"]
        .value_counts()
        .reset_index()
    )

    neg.columns = ["esporte", "quantidade"]

    fig = px.bar(
        neg,
        x="esporte",
        y="quantidade",
        title="Esportes menos preferidos"
    )

    st.plotly_chart(fig, use_container_width=True)


st.subheader("Comparação de Preferências entre Turmas")

comparacao = (
    df_filtrado
    .groupby(["ano", "ESPORTE +"])
    .size()
    .reset_index(name="quantidade")
)

fig = px.bar(
    comparacao,
    x="ESPORTE +",
    y="quantidade",
    color="ano",
    barmode="group",
    title="Preferência de esportes por ano"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Experiências Mais Marcantes nas Aulas")

exp = (
    df_filtrado["MELHOR EXPERIÊNCIA"]
    .value_counts()
    .reset_index()
)

exp.columns = ["experiencia", "quantidade"]

fig = px.pie(
    exp,
    values="quantidade",
    names="experiencia",
    title="O que os alunos consideram a melhor experiência"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Palavras que Definem a Educação Física")

palavras = (
    df_filtrado["UMA PALAVRA"]
    .value_counts()
    .reset_index()
)

palavras.columns = ["palavra", "quantidade"]

fig = px.bar(
    palavras,
    x="palavra",
    y="quantidade",
    title="Percepção dos alunos sobre a disciplina"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("Tabela de Dados")

st.dataframe(df_filtrado)
