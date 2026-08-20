import streamlit as st 
import pandas as pd 
import os
from datetime import datetime
from utils import (aplicar_cores, aplicar_filtros, limpar_filtros)  
from config import DADOS_DIR 

CAMINHO_PLANILHA = DADOS_DIR / "50_Controle_de_Protocolos_2026.xlsx" 


df = st.session_state.df.copy()
# Formatação das datas 
for coluna in ["Data Real Resp", "Data Prev Resp"]:
    if coluna in df.columns:
        df[coluna] = pd.to_datetime(
            df[coluna],
            dayfirst=True,
            errors="coerce"
        ) 
#st.write(df_exibir[["Data Entrada", "Data Real Resp ", "Data Prev Resp"]].dtypes)


# ======================
# VALORES ATUAIS DOS FILTROS
# ======================

filtro_situacao = st.session_state.get(
    "filtro_situacao",
    "Todas"
)

filtro_solicitante = st.session_state.get(
    "filtro_solicitante",
    "Todos"
)

filtro_setor = st.session_state.get(
    "filtro_setor",
    "Todos"
)


# ======================
# OPÇÕES DE CADA FILTRO
# ======================

opcoes_situacao = ["Todas"] + sorted(
    aplicar_filtros(
        df,
        solicitante=filtro_solicitante,
        setor=filtro_setor
    )["Situação"]
    .dropna()
    .astype(str)
    .unique()
)


opcoes_solicitante = ["Todos"] + sorted(
    aplicar_filtros(
        df,
        situacao=filtro_situacao,
        setor=filtro_setor
    )["Solicitante"]
    .dropna()
    .astype(str)
    .unique()
)


df_setor = aplicar_filtros(
    df,
    situacao=filtro_situacao,
    solicitante=filtro_solicitante
)


opcoes_setor = ["Todos"] + sorted(
    {
        setor.strip()
        for valor in df_setor["Responsável"].dropna()
        for setor in valor.split("/")
    }
)


# ======================
# SELECTBOXES
# ======================

col1, col2, col3, col4 = st.columns(
    [2, 2, 2, 1], 
    vertical_alignment="bottom"
    )


with col1:
    st.selectbox(
        "📌 Situação",
        opcoes_situacao,
        key="filtro_situacao"
    )


with col2:
    st.selectbox(
        "👤 Solicitante",
        opcoes_solicitante,
        key="filtro_solicitante"
    )


with col3:
    st.selectbox(
        "🏢 Setor",
        opcoes_setor,
        key="filtro_setor"
    )


with col4:
    st.button(
        "Limpar filtros",
        on_click=limpar_filtros
    )


# ======================
# PEGA OS VALORES ATUALIZADOS
# ======================

filtro_situacao = st.session_state.filtro_situacao
filtro_solicitante = st.session_state.filtro_solicitante
filtro_setor = st.session_state.filtro_setor


# ======================
# RESULTADO FINAL
# ======================

df_filtrado = aplicar_filtros(
    df,
    situacao=filtro_situacao,
    solicitante=filtro_solicitante,
    setor=filtro_setor
)


st.write(
    f"📋 {df_filtrado["Data Entrada"].count()} protocolo(s) encontrado(s)"
)

st.dataframe(
    aplicar_cores(df_filtrado),
    width="stretch", 
    column_config={
        "Data Entrada": st.column_config.DateColumn(
            format="DD/MM/YYYY"
        ),
        "Data Real Resp": st.column_config.DateColumn(
            format="DD/MM/YYYY"
        ),
        "Data Prev Resp": st.column_config.DateColumn(
            format="DD/MM/YYYY"
        ),
    },
    hide_index=True 
) 


data_arquivo = datetime.fromtimestamp(os.path.getmtime(CAMINHO_PLANILHA))
st.caption(
    f"Arquivo atualizado em: {data_arquivo.strftime('%d/%m/%Y %H:%M:%S')}"
) 
