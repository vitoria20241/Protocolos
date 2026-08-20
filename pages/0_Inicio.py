import streamlit as st
import plotly.express as px
import pandas as pd 
import io  

df = st.session_state.df

st.metric(
    "📋 Total de protocolos",
    df["Data Entrada"].count() 
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "🟪 Com prazo de resposta",
        (df["Situação"] == "Prazo de resposta").sum()
    )

with col2:
    st.metric(
        "🟥 +60 dias aberto",
        (df["Situação"] == "+60 dias aberto").sum()
    )
    
with col3:
    st.metric(
        "🟨 +45 dias aberto",
        (df["Situação"] == "+45 dias aberto").sum()
    )

with col4:
    st.metric(
        "🟩 Arquivado",
        (df["Situação"] == "Arquivado").sum()
    ) 


st.divider()
# ======================================================================

st.markdown("#### 📊 **Volume de protocolos por setor**") 
df_setores = st.session_state.df_setores

quantidade_setor = (
    df_setores["Responsável"]
    .value_counts()
    .reset_index()
)

quantidade_setor.columns = [
    "Setor",
    "Quantidade"
]


fig = px.bar(
    quantidade_setor,
    x="Setor",
    y="Quantidade",
    text="Quantidade"
)

fig.update_traces(
    textposition="outside"
)

st.plotly_chart(
    fig,
    width="stretch",
    config={
        "scrollZoom": False,
    }
)


st.caption(
    "Protocolos com mais de um setor responsável são contabilizados em cada setor."
    )

# Botão para baixar planilha excel
arquivo_excel = io.BytesIO()

with pd.ExcelWriter(
    arquivo_excel,
    engine="openpyxl"
) as writer:
    quantidade_setor.to_excel(
        writer,
        index=False,
        sheet_name="Planilha1" 
    )

arquivo_excel.seek(0)

st.download_button(
    "Exportar Excel", 
    arquivo_excel,
    "protocolos_por_setor.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
) 

st.divider()
# ======================================================================


st.markdown("####  🗂️   **Solicitantes mais frequentes**")

top5 = (
    df["Solicitante"]
    .value_counts()
    .head(9)
    .reset_index()
)

top5.columns = ["Solicitante", "Quantidade"]

cols = st.columns(3)

for i, row in top5.iterrows():
    with cols[i % 3]:
        st.metric(
            label=row["Solicitante"],
            value=row["Quantidade"],
            delta="protocolos"
        )  
