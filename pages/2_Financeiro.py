import streamlit as st
import pandas as pd
from datetime import datetime
from utils import load_data, save_data
from auth import check_password

if not check_password():
    st.stop()

st.title("💰 Gestão Financeira")

# Custom CSS for financial interface
st.markdown("""
<style>
.financial-card {
    background: linear-gradient(145deg, #ffffff, #f0f0f0);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.financial-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}
.money-input {
    font-family: 'Courier New', monospace;
    font-size: 24px !important;
    color: #2e7d32;
}
.transaction-animation {
    animation: slide-up 0.5s ease;
}
@keyframes slide-up {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
</style>
""", unsafe_allow_html=True)

# Animated tabs
tab1, tab2 = st.tabs(["💳 Nova Transação", "📊 Extrato"])

with tab1:
    st.header("Nova Movimentação")

    with st.form("registro_financeiro"):
        col1, col2 = st.columns(2)

        with col1:
            tipo = st.selectbox(
                "Tipo de Movimentação",
                ["entrada", "saída"]
            )
            valor = st.number_input("Valor", min_value=0.0, step=0.01, key="valor_input", 
                help="Digite o valor da transação")
            
            # Calculadora rápida
            col_calc1, col_calc2 = st.columns(2)
            with col_calc1:
                if st.button("+ R$ 100"):
                    st.session_state.valor_input += 100
            with col_calc2:
                if st.button("+ R$ 1000"):
                    st.session_state.valor_input += 1000

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
        # Adiciona coluna de seleção
        df_display['Selecionar'] = False
        selected_rows = st.data_editor(
            df_display,
            hide_index=True,
            column_config={
                "Selecionar": st.column_config.CheckboxColumn(default=False),
                "data": "Data",
                "tipo": "Tipo",
                "categoria": "Categoria",
                "descricao": "Descrição",
                "valor": st.column_config.NumberColumn("Valor", format="R$ %.2f")
            },
            disabled=["data", "tipo", "categoria", "descricao", "valor"]
        )
        
        # Botões de ação
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Excluir Selecionados"):
                selected_indices = selected_rows[selected_rows['Selecionar']].index
                df = df.drop(selected_indices)
                save_data(df, "financeiro")
                st.success("Registros excluídos com sucesso!")
                st.rerun()

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