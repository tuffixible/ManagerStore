import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data
from auth import check_password

if not check_password():
    st.stop()

st.title("Relatórios")

# Carregando dados
produtos_df = load_data("produtos")
financeiro_df = load_data("financeiro")

# Tabs para diferentes relatórios
tab1, tab2 = st.tabs(["Produtos", "Financeiro"])

with tab1:
    st.header("Relatório de Produtos")
    
    if not produtos_df.empty:
        # Produtos por categoria
        fig1 = px.pie(
            produtos_df,
            names='categoria',
            title='Distribuição de Produtos por Categoria'
        )
        st.plotly_chart(fig1)
        
        # Produtos com estoque baixo
        st.subheader("Produtos com Estoque Baixo (≤ 5 unidades)")
        estoque_baixo = produtos_df[produtos_df['quantidade'] <= 5]
        if not estoque_baixo.empty:
            st.dataframe(
                estoque_baixo[['nome', 'categoria', 'quantidade']],
                hide_index=True
            )
        else:
            st.info("Não há produtos com estoque baixo")
    else:
        st.info("Não há dados de produtos para gerar relatórios")

with tab2:
    st.header("Relatório Financeiro")
    
    if not financeiro_df.empty:
        # Convertendo a coluna de data
        financeiro_df['data'] = pd.to_datetime(financeiro_df['data'])
        
        # Movimentações por categoria
        fig2 = px.bar(
            financeiro_df,
            x='categoria',
            y='valor',
            color='tipo',
            title='Movimentações por Categoria'
        )
        st.plotly_chart(fig2)
        
        # Evolução temporal
        financeiro_diario = financeiro_df.groupby(
            [financeiro_df['data'].dt.date, 'tipo']
        )['valor'].sum().reset_index()
        
        fig3 = px.line(
            financeiro_diario,
            x='data',
            y='valor',
            color='tipo',
            title='Evolução das Movimentações'
        )
        st.plotly_chart(fig3)
        
        # Resumo financeiro
        st.subheader("Resumo Financeiro")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            entradas = financeiro_df[financeiro_df['tipo'] == 'entrada']['valor'].sum()
            st.metric("Total de Entradas", f"R$ {entradas:.2f}")
        
        with col2:
            saidas = financeiro_df[financeiro_df['tipo'] == 'saída']['valor'].sum()
            st.metric("Total de Saídas", f"R$ {saidas:.2f}")
        
        with col3:
            lucro = entradas - saidas
            st.metric("Lucro", f"R$ {lucro:.2f}")
    else:
        st.info("Não há dados financeiros para gerar relatórios")
