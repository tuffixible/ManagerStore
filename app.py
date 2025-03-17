import streamlit as st
import pandas as pd
from auth import check_password
import os
from datetime import datetime, timedelta

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

# Sidebar com configurações de personalização
with st.sidebar:
    st.header("Personalização do Dashboard")

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
                    st.metric("Total de Produtos", len(produtos_df))
                elif metrica == 'receitas':
                    receitas = financeiro_df[financeiro_df['tipo'] == 'entrada']['valor'].sum() if not financeiro_df.empty else 0
                    st.metric("Receitas Totais", f"R$ {receitas:.2f}")
                elif metrica == 'estoque_baixo':
                    produtos_baixo_estoque = len(produtos_df[produtos_df['quantidade'] <= 5])
                    st.metric("Produtos com Estoque Baixo", produtos_baixo_estoque)

except Exception as e:
    st.error(f"Erro ao carregar dados: {str(e)}")