import streamlit as st
import pandas as pd
from auth import check_password
import os

# Configuração inicial da página
st.set_page_config(
    page_title="Sistema de Gestão - Loja de Roupas",
    page_icon="👔",
    layout="wide"
)

# Inicialização de diretórios e arquivos
if not os.path.exists("data"):
    os.makedirs("data")

# Inicialização dos arquivos CSV se não existirem
if not os.path.exists("data/usuarios.csv"):
    pd.DataFrame({
        'usuario': ['admin'],
        'senha': ['admin123']
    }).to_csv("data/usuarios.csv", index=False)

if not os.path.exists("data/produtos.csv"):
    pd.DataFrame({
        'codigo': [],
        'nome': [],
        'categoria': [],
        'descricao': [],
        'preco_custo': [],
        'preco_venda': [],
        'quantidade': [],
        'imagem_path': []
    }).to_csv("data/produtos.csv", index=False)

if not os.path.exists("data/financeiro.csv"):
    pd.DataFrame({
        'data': [],
        'tipo': [],
        'descricao': [],
        'valor': [],
        'categoria': []
    }).to_csv("data/financeiro.csv", index=False)

# Verificação de autenticação
if not check_password():
    st.stop()

# Página principal
st.title("Sistema de Gestão - Loja de Roupas")

st.write("""
### Bem-vindo ao Sistema de Gestão
Utilize o menu lateral para navegar entre as funcionalidades:
- **Produtos**: Cadastro e gestão de produtos
- **Financeiro**: Controle de entradas e saídas
- **Relatórios**: Visualização de relatórios e gráficos
""")

# Métricas principais
col1, col2, col3 = st.columns(3)

# Carregando dados
produtos_df = pd.read_csv("data/produtos.csv")
financeiro_df = pd.read_csv("data/financeiro.csv")

with col1:
    st.metric("Total de Produtos", len(produtos_df))

with col2:
    if not financeiro_df.empty:
        receitas = financeiro_df[financeiro_df['tipo'] == 'entrada']['valor'].sum()
        st.metric("Receitas Totais", f"R$ {receitas:.2f}")
    else:
        st.metric("Receitas Totais", "R$ 0.00")

with col3:
    produtos_baixo_estoque = len(produtos_df[produtos_df['quantidade'] <= 5])
    st.metric("Produtos com Estoque Baixo", produtos_baixo_estoque)
