import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import ipeadatapy as ip

# Configurações iniciais da página
st.set_page_config(
    page_title="ListaExercicio4",
    layout="centered"
)

st.title("Projeto Final - Análise Contábil com Ajuste Econômico")
st.write("""Este projeto tem como objetivo integrar análise de dados contábeis de empresas com indicadores econômicos,
utilizando Python, Pandas, Ipeadata e Streamlit.
""")

# Carregamento dos dados das empresas
df = pd.read_csv("empresas_dados.csv", sep=';')
st.subheader("📄 Dados das Empresas")
st.dataframe(df.head(len(df)))

# Cálculo dos indicadores
st.subheader("📊 Indicadores Financeiros: Margem Líquida e ROA")
df["Margem Líquida"] = (df["Lucro Líquido"] / df["Receita Líquida"]) * 100
df["ROA"] = (df["Lucro Líquido"] / df["Ativo Total"]) * 100

df_grouped = df.groupby("Ano")[["Margem Líquida", "ROA"]].mean().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(df_grouped["Ano"], df_grouped["Margem Líquida"], label="Margem Líquida")
ax1.plot(df_grouped["Ano"], df_grouped["ROA"], label="ROA")
ax1.set_xlabel("Ano")
ax1.set_ylabel("%")
ax1.set_title("Margem Líquida e ROA por Ano (média das empresas)")
ax1.legend()
ax1.grid(True)
st.pyplot(fig1)

# Obtenção dos dados de IPCA
st.subheader("📈 IPCA - Variação Anual (%)")
ipca = ip.timeseries('PRECOS_IPCAG', yearGreaterThan=2009, yearSmallerThan=2025)
ipca = ipca.rename(columns={
    "YEAR": "Ano",
    "VALUE ((% a.a.))": "IPCA"
})
st.dataframe(ipca)

# Combinar dados das empresas com IPCA
df_combinado = pd.merge(df, ipca, on="Ano")
df_combinado["Receita Real"] = df_combinado["Receita Líquida"] - (df_combinado["Receita Líquida"] * (df_combinado["IPCA"] / 100))

st.subheader("🧮 Receita Real (ajustada pelo IPCA)")
st.dataframe(df_combinado[["Ano", "Empresa", "Receita Líquida", "IPCA", "Receita Real"]])

# Gráfico Receita Líquida vs Receita Real
grafico_df = df_combinado.groupby("Ano")[["Receita Líquida", "Receita Real"]].sum().reset_index()

fig2, ax2 = plt.subplots(figsize=(10, 5))
ax2.plot(grafico_df["Ano"], grafico_df["Receita Líquida"], marker='o', label="Receita Líquida")
ax2.plot(grafico_df["Ano"], grafico_df["Receita Real"], marker='s', label="Receita Real")
ax2.set_xlabel("Ano")
ax2.set_ylabel("Valor (R$)")
ax2.set_title("Receita Líquida vs Receita Real por Ano")
ax2.grid(True)
ax2.legend()
st.pyplot(fig2)

