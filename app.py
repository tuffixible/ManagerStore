
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
    try:
        if os.path.exists("logo.png"):
            st.image("logo.png", width=300)
    except:
        pass

# Inicialização de diretórios
os.makedirs("data", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

# Verificação de autenticação
if not check_password():
    st.stop()

# Cards informativos com efeitos visuais
st.markdown("""
<style>
.metric-card {
    background: linear-gradient(145deg, #ffffff, #f0f0f0);
    border-radius: 15px;
    padding: 20px;
    box-shadow: 10px 10px 20px #d1d1d1, -10px -10px 20px #ffffff;
    margin: 10px 0;
    transition: transform 0.3s ease;
}
.metric-card:hover {
    transform: translateY(-5px);
}
.st-emotion-cache, div.st-emotion-cache-x78sv8, div.st-emotion-cache-r421ms {
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

try:
    produtos_df = pd.read_csv("data/produtos.csv")
    financeiro_df = pd.read_csv("data/financeiro.csv")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h3>📦 Total de Produtos</h3>
            <h2>{}</h2>
        </div>
        """.format(len(produtos_df)), unsafe_allow_html=True)

    with col2:
        receitas = financeiro_df[financeiro_df['tipo'] == 'entrada']['valor'].sum() if not financeiro_df.empty else 0
        st.markdown("""
        <div class="metric-card">
            <h3>💰 Receitas Totais</h3>
            <h2>R$ {:.2f}</h2>
        </div>
        """.format(receitas), unsafe_allow_html=True)

    with col3:
        produtos_baixo_estoque = len(produtos_df[produtos_df['quantidade'] <= 5])
        st.markdown("""
        <div class="metric-card">
            <h3>⚠️ Produtos com Estoque Baixo</h3>
            <h2>{}</h2>
        </div>
        """.format(produtos_baixo_estoque), unsafe_allow_html=True)

except Exception as e:
    st.warning("Aguarde um momento enquanto os dados são carregados...")

# Menu de navegação com efeitos visuais
st.sidebar.markdown("""
<style>
.sidebar-menu {
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
    transition: all 0.3s ease;
}
.sidebar-menu:hover {
    background: #f0f2f6;
    transform: scale(1.02);
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("Menu Principal")
st.sidebar.markdown("""
<div class="sidebar-menu">🏠 <b>Home</b>: Página inicial</div>
<div class="sidebar-menu">💰 <b>Financeiro</b>: Controle de caixa</div>
<div class="sidebar-menu">📊 <b>Relatórios</b>: Análises e gráficos</div>
<div class="sidebar-menu">🤖 <b>Assistente IA</b>: Sugestões</div>
<div class="sidebar-menu">⚙️ <b>Configurações</b>: Personalização</div>
""", unsafe_allow_html=True)

st.write("""
### 👋 Bem-vindo ao Sistema!
Utilize o menu lateral para acessar todas as funcionalidades disponíveis.
""")
