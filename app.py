import streamlit as st
import pandas as pd
from auth import check_password
import os
from datetime import datetime, timedelta
import random

# Configuração inicial da página
st.set_page_config(
    page_title="Sistema de Gestão - Loja de Roupas",
    page_icon="👔",
    layout="wide"
)

# CSS para easter eggs
st.markdown("""
<style>
@keyframes celebrate {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
}

.celebration {
    animation: celebrate 0.5s ease-in-out;
    display: inline-block;
}

.hidden-message {
    opacity: 0;
    transition: opacity 0.3s;
}

.hidden-message:hover {
    opacity: 1;
}

.sparkle {
    position: relative;
}

.sparkle::after {
    content: '✨';
    position: absolute;
    top: -10px;
    right: -10px;
    font-size: 14px;
    opacity: 0;
    transition: opacity 0.3s;
}

.sparkle:hover::after {
    opacity: 1;
}
</style>
""", unsafe_allow_html=True)

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

# Inicialização do estado da sessão para configurações de personalização
if 'show_metricas' not in st.session_state:
    st.session_state.show_metricas = {
        'total_produtos': True,
        'receitas': True,
        'estoque_baixo': True
    }

if 'periodo_analise' not in st.session_state:
    st.session_state.periodo_analise = '30'

# Página principal
st.title("Sistema de Gestão - Loja de Roupas")

# Easter egg: Mensagens motivacionais aleatórias
mensagens_motivacionais = [
    "✨ Dica secreta: Sorria para seus clientes, faz toda diferença!",
    "🌟 Lembre-se: Cada venda é uma história de sucesso",
    "🎯 O segredo do sucesso está nos pequenos detalhes",
    "🚀 Grandes negócios começam com pequenos passos",
    "💫 Você está fazendo um ótimo trabalho!"
]

# Easter egg: Mostrar mensagem motivacional com 20% de chance
if random.random() < 0.2:
    st.sidebar.markdown(
        f"""
        <div class="hidden-message" style="padding: 10px; background: #f0f2f6; border-radius: 5px; margin: 10px 0;">
            {random.choice(mensagens_motivacionais)}
        </div>
        """,
        unsafe_allow_html=True
    )

# Sidebar com configurações de personalização
with st.sidebar:
    st.header("Personalização do Dashboard")

    # Easter egg: Contador de cliques oculto
    if 'click_count' not in st.session_state:
        st.session_state.click_count = 0

    if st.button("✨", key="easter_egg_button"):
        st.session_state.click_count += 1
        if st.session_state.click_count == 5:
            st.balloons()
            st.success("🎉 Você descobriu um segredo! Continue explorando!")
            st.session_state.click_count = 0

    # Seleção de métricas visíveis
    st.subheader("Métricas Visíveis")
    st.session_state.show_metricas['total_produtos'] = st.checkbox(
        "Total de Produtos",
        value=st.session_state.show_metricas['total_produtos']
    )
    st.session_state.show_metricas['receitas'] = st.checkbox(
        "Receitas Totais",
        value=st.session_state.show_metricas['receitas']
    )
    st.session_state.show_metricas['estoque_baixo'] = st.checkbox(
        "Produtos com Estoque Baixo",
        value=st.session_state.show_metricas['estoque_baixo']
    )

    # Período de análise
    st.subheader("Período de Análise")
    st.session_state.periodo_analise = st.selectbox(
        "Selecione o período",
        options=['7', '15', '30', '90', 'todos'],
        format_func=lambda x: f"Últimos {x} dias" if x != 'todos' else "Todo o período",
        index=['7', '15', '30', '90', 'todos'].index(st.session_state.periodo_analise)
    )

st.write("""
### Bem-vindo ao Sistema de Gestão
Utilize o menu lateral para navegar entre as funcionalidades:
- **Produtos**: Cadastro e gestão de produtos
- **Financeiro**: Controle de entradas e saídas
- **Relatórios**: Visualização de relatórios e gráficos
""")

try:
    # Carregando dados
    produtos_df = pd.read_csv("data/produtos.csv")
    financeiro_df = pd.read_csv("data/financeiro.csv")

    # Filtrando dados pelo período selecionado
    if st.session_state.periodo_analise != 'todos':
        dias = int(st.session_state.periodo_analise)
        data_limite = datetime.now() - timedelta(days=dias)
        financeiro_df['data'] = pd.to_datetime(financeiro_df['data'])
        financeiro_df = financeiro_df[financeiro_df['data'] >= data_limite]

    # Layout dinâmico das métricas baseado nas configurações
    metricas_ativas = [k for k, v in st.session_state.show_metricas.items() if v]
    if metricas_ativas:
        cols = st.columns(len(metricas_ativas))

        for i, (col, metrica) in enumerate(zip(cols, metricas_ativas)):
            with col:
                if metrica == 'total_produtos':
                    # Easter egg: Adicionar classe sparkle em números redondos
                    total_produtos = len(produtos_df)
                    if total_produtos % 10 == 0:
                        st.markdown(f"""
                            <div class="sparkle">
                                <h3>Total de Produtos: {total_produtos}</h3>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.metric("Total de Produtos", total_produtos)

                elif metrica == 'receitas':
                    receitas = financeiro_df[financeiro_df['tipo'] == 'entrada']['valor'].sum() if not financeiro_df.empty else 0
                    # Easter egg: Celebrar quando as receitas são maiores que 10000
                    if receitas > 10000:
                        st.markdown(f"""
                            <div class="celebration">
                                <h3>🎉 Receitas Totais: R$ {receitas:.2f}</h3>
                            </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.metric("Receitas Totais", f"R$ {receitas:.2f}")

                elif metrica == 'estoque_baixo':
                    produtos_baixo_estoque = len(produtos_df[produtos_df['quantidade'] <= 5])
                    st.metric("Produtos com Estoque Baixo", produtos_baixo_estoque)

except Exception as e:
    st.error(f"Erro ao carregar dados: {str(e)}")