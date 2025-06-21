import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import ipeadatapy as ip

"""1) Configure o título na barra do navegador, da página do projeto no Streamlit e descrição inicial do projeto (peso: 1,0)

Título na barra (page_title): Lista de Exercícios 4
Título da página (header): Projeto Final – Análise Contábil com Ajuste Econômico
Descrição projeto (write): Este projeto tem como objetivo integrar análise de dados contábeis de empresas com indicadores econômicos, utilizando Python, Pandas, Ipeadata e Streamlit."""
st.set_page_config(
    page_title="ListaExercicio4",
    layout="centered"
)

st.title("Projeto Final - Análise Contábil com Ajuste Econômico")
st.write("""Este projeto tem como objetivo integrar análise de dados contábeis de empresas com indicadores econômicos,
utilizando Python, Pandas, Ipeadata e Streamlit.
""")

"""2) Importe os dados do arquivo empresas_dados.csv utilizando pandas e apresente todas as linhas da df (peso: 1,0)

Dica: Utilize head(len(df))"""
df = pd.read_csv("empresas_dados.csv", sep=';')
st.subheader("📄 Dados das Empresas")
st.dataframe(df.head(len(df)))

"""3) Calcule os indicadores Margem Líquida e ROA e salve como novas coluna da df. Depois apresente os dois indicadores no mesmo gráfico de linhas, agrupado por Ano  (peso: 1,0)

- Margem Líquida = Lucro Líquido / Receita Líquida * 100
- ROA = Lucro Líquido / Ativo Total *  100
"""
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

"""4) Utilize o pacote ipeadatapy e faça busca para encontrar o indicador que traga o IPCA, taxa de variação, em % e anual: (peso: 2,0)

- Baixe os dados no período de 2010 a 2024
- Altere o nome da coluna "YEAR" para "Ano"
- Altere o nome da coluna "VALUE ((% a.a.))" para "IPCA"
- Apresente a df para checar se tudo deu certo
"""
st.subheader("📈 IPCA - Variação Anual (%)")
ipca = ip.timeseries('PRECOS_IPCAG', yearGreaterThan=2009, yearSmallerThan=2025)
ipca = ipca.rename(columns={
    "YEAR": "Ano",
    "VALUE ((% a.a.))": "IPCA"
})
st.dataframe(ipca)

"""5) Combine as duas df (Excel e IPEA) em uma nova df e calcule nova coluna chamada Receita Real (peso: 2,0)

- Utilize a função pd.merge() para unificar as duas df utiilizando a coluna Ano como conexão (chave primária) entre elas
- Crie nova coluna chamada Receita Real que será o resultado da Receita Líquida de cada ano deduzido o IPCA do ano: Receita Real = Receitta Líquida - ( Receita Líquida * (IPCA/100) )
- Apresente a nova df combinada

"""
df_combinado = pd.merge(df, ipca, on="Ano")
df_combinado["Receita Real"] = df_combinado["Receita Líquida"] - (df_combinado["Receita Líquida"] * (df_combinado["IPCA"] / 100))

st.subheader("🧮 Receita Real (ajustada pelo IPCA)")
st.dataframe(df_combinado[["Ano", "Empresa", "Receita Líquida", "IPCA", "Receita Real"]])

"""6) Crie gráfico de linha que apresente as variáveis Receita Líquida e Receita Real ao longo dos anos (no mesmo gráfico) (peso: 1,0)"""

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

