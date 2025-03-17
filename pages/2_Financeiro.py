import streamlit as st
import pandas as pd
from datetime import datetime
from utils import load_data, save_data
from auth import check_password

if not check_password():
    st.stop()

st.title("Gestão Financeira")

# Tabs para diferentes funcionalidades
tab1, tab2 = st.tabs(["Registro de Movimentação", "Extrato"])

with tab1:
    st.header("Nova Movimentação")

    with st.form("registro_financeiro"):
        col1, col2 = st.columns(2)

        with col1:
            tipo = st.selectbox(
                "Tipo de Movimentação",
                ["entrada", "saída"]
            )
            valor = st.number_input("Valor", min_value=0.0, step=0.01)

        with col2:
            categoria = st.selectbox(
                "Categoria",
                ["Vendas", "Fornecedores", "Funcionários", "Outros"]
            )
            descricao = st.text_input("Descrição")

        submitted = st.form_submit_button("Registrar")

        if submitted:
            if valor > 0:
                df = load_data("financeiro")

                nova_movimentacao = {
                    'data': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'tipo': tipo,
                    'descricao': descricao,
                    'valor': valor,
                    'categoria': categoria
                }

                df = pd.concat([df, pd.DataFrame([nova_movimentacao])], ignore_index=True)
                save_data(df, "financeiro")
                st.success("Movimentação registrada com sucesso!")
            else:
                st.error("O valor deve ser maior que zero")

with tab2:
    st.header("Extrato Financeiro")

    df = load_data("financeiro")

    if not df.empty:
        # Filtros
        col1, col2 = st.columns(2)

        with col1:
            tipo_filter = st.multiselect(
                "Filtrar por Tipo",
                options=df['tipo'].unique()
            )

        with col2:
            categoria_filter = st.multiselect(
                "Filtrar por Categoria",
                options=df['categoria'].unique()
            )

        # Aplicar filtros
        if tipo_filter:
            df = df[df['tipo'].isin(tipo_filter)]
        if categoria_filter:
            df = df[df['categoria'].isin(categoria_filter)]

        # Exibir movimentações
        df_display = df[['data', 'tipo', 'categoria', 'descricao', 'valor']]
        st.dataframe(
            data=df_display,
            hide_index=True
        )

        # Resumo
        col1, col2, col3 = st.columns(3)

        with col1:
            entradas = df[df['tipo'] == 'entrada']['valor'].sum()
            st.metric("Total de Entradas", f"R$ {entradas:.2f}")

        with col2:
            saidas = df[df['tipo'] == 'saída']['valor'].sum()
            st.metric("Total de Saídas", f"R$ {saidas:.2f}")

        with col3:
            saldo = entradas - saidas
            st.metric("Saldo", f"R$ {saldo:.2f}")

        # Exportar dados
        if st.button("Exportar para CSV"):
            df.to_csv("extrato.csv", index=False)
            st.success("Dados exportados com sucesso!")
    else:
        st.info("Nenhuma movimentação registrada")