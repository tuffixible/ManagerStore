import streamlit as st
import pandas as pd
from auth import check_password
import os

# Configuração inicial da página
st.set_page_config(
    page_title="Home - Loja Xible",
    page_icon="🏠",
    layout="wide"
)

# Logo e título
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("Sistema de Gestão - Loja Xible")
    try:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=200)
    except:
        st.info("⚠️ Logo não encontrada. Faça upload do arquivo logo.png para personalizar.")

# Inicialização de diretórios
os.makedirs("data", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

# Estrutura dos DataFrames
produtos_structure = {
    'codigo': [],
    'nome': [],
    'categoria': [],
    'descricao': [],
    'preco_custo': [],
    'preco_venda': [],
    'quantidade': [],
    'imagem_path': [],
    'tamanho': []  # Adicionando 'tamanho' na estrutura
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

# Cards informativos
col1, col2, col3 = st.columns(3)

try:
    produtos_df = pd.read_csv("data/produtos.csv")
    financeiro_df = pd.read_csv("data/financeiro.csv")

    # Convertendo a coluna 'tamanho' para int
    if 'tamanho' in produtos_df.columns:
        produtos_df['tamanho'] = produtos_df['tamanho'].astype(int)

    with col1:
        st.metric("Total de Produtos", len(produtos_df))

    with col2:
        receitas = financeiro_df[financeiro_df['tipo'] == 'entrada']['valor'].sum() if not financeiro_df.empty else 0
        st.metric("Receitas Totais", f"R$ {receitas:.2f}")

    with col3:
        produtos_baixo_estoque = len(produtos_df[produtos_df['quantidade'] <= 5])
        st.metric("Produtos com Estoque Baixo", produtos_baixo_estoque)

except Exception as e:
    st.error("Erro ao carregar dados")

# Menu de navegação
st.sidebar.title("Menu Principal")
st.sidebar.markdown("""
- 📦 **Produtos**: Cadastro e gestão
- 💰 **Financeiro**: Controle de caixa
- 📊 **Relatórios**: Análises e gráficos
- 🤖 **Assistente IA**: Sugestões
- ⚙️ **Configurações**: Personalização
""")



# Mensagem de boas-vindas
st.write("""
### Bem-vindo ao Sistema!
Utilize o menu lateral para acessar todas as funcionalidades disponíveis.
""")

# Editando e mostrando o DataFrame de produtos
st.header("Gerenciar Produtos")
if st.button("Carregar Produtos"):
    edited_df = st.data_editor(
        produtos_df,
        column_config={
            'codigo': st.column_config.TextColumn(),
            'nome': st.column_config.TextColumn(),
            'categoria': st.column_config.TextColumn(),
            'descricao': st.column_config.TextColumn(),
            'preco_custo': st.column_config.NumberColumn(),
            'preco_venda': st.column_config.NumberColumn(),
            'quantidade': st.column_config.NumberColumn(),
            'imagem_path': st.column_config.TextColumn(),
            'tamanho': st.column_config.NumberColumn()  # Garantindo que Tamanho seja tratado como coluna numérica
        }
    )

    # Exibir o DataFrame editado
    st.write(edited_df)