# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 09:59:16 2026

@author: vitoria.bulhoes
"""

import streamlit as st
import pandas as pd

from config import ASSETS_DIR 

LOGO = ASSETS_DIR / "logo.png"

st.set_page_config(
    page_title="Eventos",
    page_icon="LOGO",
    layout="wide"
)

st.markdown("### Eventos")


df_eventos = st.session_state.df_eventos.copy()

# Formatar datas 
for coluna in ["Data inscrição", "Data do evento"]:
    if coluna in df_eventos.columns:
        df_eventos[coluna] = pd.to_datetime(
            df_eventos[coluna],
            dayfirst=True,
            errors="coerce"
        ).dt.strftime("%d/%m/%Y")

# ============================================================
# FILTROS 
# ============================================================

participantes = (
    df_eventos["Participantes"]
    .dropna()
    .astype(str)
    .str.split("/")
    .explode()
    .str.strip()
)

participantes = sorted(
    participantes[participantes != ""].unique()
)


col1, col2 = st.columns([2,1]) 
with col1:
    filtro_participantes = st.multiselect(
    "Participante",
    participantes,
    placeholder="Selecione um ou mais participantes"
)



df_filtrado = df_eventos.copy()


if filtro_participantes:

    df_filtrado = df_filtrado[
        df_filtrado["Participantes"]
        .fillna("")
        .apply(
            lambda x: any(
                participante in [
                    p.strip()
                    for p in str(x).split("/")
                ]
                for participante in filtro_participantes
            )
        )
    ]


# ============================================================
# TABELA
# ============================================================

st.write(
    f"📋 {df_filtrado["Evento"].count()} evento(s) encontrado(s)"
)

st.dataframe(
    df_filtrado,
    hide_index=True,
    ) 
