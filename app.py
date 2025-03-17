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

# Inicialização de diretórios
os.makedirs("data", exist_ok=True)

# Estrutura dos DataFrames
produtos_structure = {
    'codigo': [],
    'nome': [],
    'categoria': [],
    'descricao': [],
    'preco_custo': [],
    'preco_venda': [],
    'quantidade': [],
    'imagem_path': []
}

financeiro_structure = {
    'data': [],
    'tipo': [],
    'descricao': [],
    'valor': [],
    'categoria': []
}

usuarios_structure = {
    'usuario': ['admin'],
    'senha': ['admin123']
}

# Inicialização dos arquivos CSV
if not os.path.exists("data/usuarios.csv"):
    pd.DataFrame(usuarios_structure).to_csv("data/usuarios.csv", index=False)

if not os.path.exists("data/produtos.csv"):
    pd.DataFrame(produtos_structure).to_csv("data/produtos.csv", index=False)

if not os.path.exists("data/financeiro.csv"):
    pd.DataFrame(financeiro_structure).to_csv("data/financeiro.csv", index=False)

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

try:
    # Métricas principais
    col1, col2, col3 = st.columns(3)

    # Carregando dados
    produtos_df = pd.read_csv("data/produtos.csv")
    financeiro_df = pd.read_csv("data/financeiro.csv")

    with col1:
        st.metric("Total de Produtos", len(produtos_df))

    with col2:
        receitas = financeiro_df[financeiro_df['tipo'] == 'entrada']['valor'].sum() if not financeiro_df.empty else 0
        st.metric("Receitas Totais", f"R$ {receitas:.2f}")

    with col3:
        produtos_baixo_estoque = len(produtos_df[produtos_df['quantidade'] <= 5])
        st.metric("Produtos com Estoque Baixo", produtos_baixo_estoque)
except Exception as e:
    st.error(f"Erro ao carregar dados: {str(e)}")