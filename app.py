# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 10:14:28 2026

@author: vitoria.bulhoes
"""

import streamlit as st
import pandas as pd
from utils import (atualizar_protocolo, atualizar_status, 
                   criar_situacao, criar_base_setores, limpar_solicitante)  
from config import (DADOS_DIR, ASSETS_DIR) 

CAMINHO_PLANILHA = DADOS_DIR / "50_Controle_de_Protocolos_2026.xlsx"  
LOGO = ASSETS_DIR / "logo.png"
LOGO1 = ASSETS_DIR / "logo1.png"


if "df" not in st.session_state:
    df = pd.read_excel(CAMINHO_PLANILHA,
                       dtype = {"Nº Protocolo": str})  
    df = atualizar_protocolo(df)
    df = atualizar_status(df) 
    df = criar_situacao(df) 
    df = limpar_solicitante(df) 
    st.session_state.df = df
    
    df_setores = criar_base_setores(df)
    st.session_state.df_setores = df_setores
    
    
st.set_page_config(
    page_title="Protocolos",
    page_icon=str(LOGO), 
    layout="wide"
)

st.sidebar.image(str(LOGO1), width=70) 

pg = st.navigation([
    st.Page("pages/0_Inicio.py", title="⌂ Início"),
    st.Page("pages/1_Consulta.py", title="◫ Consulta"),
])

pg.run() 