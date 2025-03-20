
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

# Add global bird animation CSS
st.markdown("""
<style>
.fashion-item {
    position: fixed;
    font-size: 32px;
    z-index: 1000;
    transform-origin: center;
    animation: float 15s linear infinite;
    cursor: pointer;
    text-shadow: 0 0 5px rgba(255,255,255,0.8);
}
@keyframes float {
    0% { 
        left: -50px; 
        top: 100px; 
        transform: scaleX(1) rotate(15deg); 
    }
    23% { 
        left: 40%; 
        top: 80%; 
        transform: scaleX(1) rotate(-5deg); 
    }
    25% { 
        left: 45%; 
        top: 75%; 
        transform: scaleX(-1) rotate(5deg); 
    }
    48% { 
        left: 95%; 
        top: 30%; 
        transform: scaleX(-1) rotate(-10deg); 
    }
    50% { 
        left: 95%; 
        top: 35%; 
        transform: scaleX(-1) rotate(5deg); 
    }
    73% { 
        left: 45%; 
        top: 20%; 
        transform: scaleX(-1) rotate(-5deg); 
    }
    75% { 
        left: 40%; 
        top: 25%; 
        transform: scaleX(1) rotate(5deg); 
    }
    98% { 
        left: -45px; 
        top: 95px; 
        transform: scaleX(1) rotate(-5deg); 
    }
    100% { 
        left: -50px; 
        top: 100px; 
        transform: scaleX(1) rotate(15deg); 
    }
}
@keyframes flap {
    0%, 100% { transform: scale(1, 1) translateY(0); }
    25% { transform: scale(1.1, 0.9) translateY(-2px); }
    50% { transform: scale(1, 1) translateY(0); }
    75% { transform: scale(1.1, 0.9) translateY(2px); }
}
</style>
""", unsafe_allow_html=True)

# Add bird if enabled in session state
if 'show_easter_egg' not in st.session_state:
    st.session_state.show_easter_egg = True

if st.session_state.show_easter_egg:
    import random
    fashion_items = ['👕', '👖', '👗', '👚', '👔', '👠', '👟', '👢', '👜', '🧢']
    random_item = random.choice(fashion_items)
    st.markdown(f"""
        <div class="fashion-item" onclick="this.style.animationPlayState=this.style.animationPlayState==='paused'?'running':'paused'">
            {random_item}
        </div>
    """, unsafe_allow_html=True)

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

# Controle de acesso baseado no perfil
if 'user_role' not in st.session_state:
    st.error("Erro de sessão. Por favor, faça login novamente.")
    st.stop()

user_role = st.session_state.get('user_role', 'vendedor')
if user_role not in ['administrador', 'gerente', 'vendedor']:
    st.error("Perfil de usuário inválido")
    st.stop()

# Customização baseada no perfil
if user_role == 'administrador':
    st.sidebar.success("🔑 Acesso Administrativo")
elif user_role == 'gerente':
    st.sidebar.info("👔 Acesso Gerencial")
else:
    st.sidebar.info("👤 Acesso Vendedor")

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
<div class="sidebar-menu">🛍️ <b>Loja</b>: Vitrine de produtos</div>
""", unsafe_allow_html=True)

st.write("""
### 👋 Bem-vindo ao Sistema!
Utilize o menu lateral para acessar todas as funcionalidades disponíveis.
""")
