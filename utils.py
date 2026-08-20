# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 10:59:20 2026

@author: vitoria.bulhoes
"""

import pandas as pd
import streamlit as st

def atualizar_protocolo(df): 
    # Reescreve a coluna N° Protocolo adicionando /ANO 
    
    # Converte a coluna para datetime, mantendo vazios como NaT
    df["Data Entrada"] = pd.to_datetime(
        df["Data Entrada"],
        dayfirst=True,
        errors="coerce"
    )

    # Apenas linhas que possuem Data Entrada
    mask = df["Data Entrada"].notna()

    df.loc[mask, "Nº Protocolo"] = (
        df.loc[mask, "Nº Protocolo"]
        .astype(str)
        .str.split("/")
        .str[0]
        + "/"
        + df.loc[mask, "Data Entrada"].dt.year.astype(str)
    )

    return df 


def atualizar_status(df): 
    # Considera Arquivado caso a coluna Data Real Resp esteja preenchida 
    
    mask = df["Data Real Resp"].notna()
    df.loc[mask, "Status"] = "Arquivado"
    return df 


def criar_situacao(df):
    # Cria a coluna Situação 
    
    hoje = pd.Timestamp.today()

    df["Situação"] = ""

    # Arquivado
    df.loc[
        df["Status"] == "Arquivado",
        "Situação"
    ] = "Arquivado"

    # Possui prazo de resposta
    df.loc[
        (df["Data Prev Resp"].notna()) &
        (df["Data Real Resp"].isna()),
        "Situação"
    ] = "Prazo de resposta"

    # Dias em aberto
    dias = (hoje - df["Data Entrada"]).dt.days

    df.loc[
        (dias > 60) & (df["Situação"] == ""),
        "Situação"
    ] = "+60 dias aberto"

    df.loc[
        (dias > 45) & (dias <= 60) & (df["Situação"] == ""),
        "Situação"
    ] = "+45 dias aberto"
    
    # O que não se encaixou em nenhuma regra
    df.loc[
        df["Situação"] == "",
        "Situação"
    ] = "Outro" 

    # coloca Situação como primeira coluna
    coluna = df.pop("Situação")
    df.insert(0, "Situação", coluna)

    return df


def aplicar_cores(df):
    # Define as cores com base na coluna Situação 

    def cor_linha(row):
        estilo = [""] * len(row)

        idx = df.columns.get_loc("Situação")

        cores = {
            "Arquivado": "#e8f5e9",
            "Prazo de resposta": "#ddd6fe",
            "+60 dias aberto": "#ffcdd2",
            "+45 dias aberto": "#fff9c4"
        }

        if row["Situação"] in cores:
            estilos = cores[row["Situação"]]
            estilo[idx] = f"background-color: {estilos}"

        return estilo

    return df.style.apply(cor_linha, axis=1) 


def criar_base_setores(df):
    # Cria dataframe auxiliar para o gráfico protocolos x setor 
    
    df_setores = (
        df[["Nº Protocolo", "Responsável"]]
        .copy()
    )

    # separa os setores
    df_setores["Responsável"] = (
        df_setores["Responsável"]
        .fillna("")
        .str.split("/")
    )

    # cria uma linha para cada setor
    df_setores = df_setores.explode("Responsável")

    # limpa espaços
    df_setores["Responsável"] = (
        df_setores["Responsável"]
        .str.strip()
    )

    # remove vazios
    df_setores = df_setores[
        df_setores["Responsável"] != ""
    ]

    return df_setores 


def limpar_solicitante(df):
    # Formata a coluna "Solicitante" 
    if "Solicitante" in df.columns:
        df["Solicitante"] = (
            df["Solicitante"]
            .str.strip()
            .str.title()
        )
    return df  


def aplicar_filtros(df, situacao=None, solicitante=None, setor=None):
    # Funcao para fazer filtros cascata na pagina de consulta 
    df = df.copy()

    if situacao and situacao != "Todas":
        df = df[df["Situação"] == situacao]

    if solicitante and solicitante != "Todos":
        df = df[df["Solicitante"] == solicitante]

    if setor and setor != "Todos":
        df = df[df["Responsável"].str.contains(setor, na=False)]

    return df 


def limpar_filtros():
    st.session_state["filtro_situacao"] = "Todas"
    st.session_state["filtro_solicitante"] = "Todos"
    st.session_state["filtro_setor"] = "Todos" 