import pandas as pd
import streamlit as st
from datetime import datetime
import base64

def load_data(file_name):
    """Carrega dados do arquivo CSV"""
    try:
        return pd.read_csv(f"data/{file_name}.csv")
    except:
        return pd.DataFrame()

def save_data(df, file_name):
    """Salva dados no arquivo CSV"""
    df.to_csv(f"data/{file_name}.csv", index=False)

def format_currency(value):
    """Formata valor para moeda brasileira"""
    return f"R$ {value:.2f}"

def get_image_base64(image_file):
    """Converte imagem para base64"""
    return base64.b64encode(image_file.getvalue()).decode()

def validate_product_data(nome, preco_custo, preco_venda, quantidade):
    """Valida dados do produto"""
    if not nome:
        st.error("Nome do produto é obrigatório")
        return False
    try:
        preco_custo = float(preco_custo)
        preco_venda = float(preco_venda)
        quantidade = int(quantidade)
        if preco_custo < 0 or preco_venda < 0 or quantidade < 0:
            st.error("Valores não podem ser negativos")
            return False
    except:
        st.error("Valores inválidos")
        return False
    return True
