import streamlit as st
import pandas as pd
from utils import load_data, save_data, validate_product_data
from auth import check_password

if not check_password():
    st.stop()

st.title("Gestão de Produtos")

# Tabs para diferentes funcionalidades
tab1, tab2, tab3 = st.tabs(["Cadastro", "Lista de Produtos", "Controle de Estoque"])

with tab1:
    st.header("Cadastro de Produtos")
    
    with st.form("cadastro_produto"):
        if st.session_state.get('mobile_view', False):
            # Layout para mobile: uma coluna
            nome = st.text_input("Nome do Produto")
            categoria = st.selectbox(
                "Categoria",
                ["Roupas", "Calçados", "Acessórios"]
            )
            cor = st.text_input("Cor")
            tamanho = st.text_input("Tamanho")
            preco_custo = st.number_input("Preço de Custo", min_value=0.0, step=0.01)
            preco_venda = st.number_input("Preço de Venda", min_value=0.0, step=0.01)
            quantidade = st.number_input("Quantidade em Estoque", min_value=0, step=1)
            descricao = st.text_area("Descrição")
            imagem = st.file_uploader("Imagem do Produto", type=['jpg', 'jpeg', 'png'])
        else:
            # Layout para desktop: duas colunas
            col1, col2 = st.columns(2)
            with col1:
                nome = st.text_input("Nome do Produto")
                categoria = st.selectbox(
                    "Categoria",
                    ["Roupas", "Calçados", "Acessórios"]
                )
                cor = st.text_input("Cor")
                tamanho = st.text_input("Tamanho")
                preco_custo = st.number_input("Preço de Custo", min_value=0.0, step=0.01)
                preco_venda = st.number_input("Preço de Venda", min_value=0.0, step=0.01)
            
            with col2:
                quantidade = st.number_input("Quantidade em Estoque", min_value=0, step=1)
                descricao = st.text_area("Descrição")
                imagem = st.file_uploader("Imagem do Produto", type=['jpg', 'jpeg', 'png'])
        
        submitted = st.form_submit_button("Cadastrar Produto")
        
        if submitted:
            if validate_product_data(nome, preco_custo, preco_venda, quantidade):
                # Salvar imagem se existir
                if imagem:
                    with open(f"uploads/{imagem.name}", "wb") as f:
                        f.write(imagem.getbuffer())
                df = load_data("produtos")
                
                novo_produto = {
                    'codigo': len(df) + 1,
                    'nome': nome,
                    'categoria': categoria,
                    'cor': cor,
                    'tamanho': tamanho,
                    'descricao': descricao,
                    'preco_custo': preco_custo,
                    'preco_venda': preco_venda,
                    'quantidade': quantidade,
                    'imagem_path': imagem.name if imagem else ''
                }
                
                df = pd.concat([df, pd.DataFrame([novo_produto])], ignore_index=True)
                save_data(df, "produtos")
                st.success("Produto cadastrado com sucesso!")

with tab2:
    st.header("Lista de Produtos")
    
    df = load_data("produtos")
    
    if not df.empty:
        # Filtros
        col1, col2 = st.columns(2)
        with col1:
            categoria_filter = st.multiselect(
                "Filtrar por Categoria",
                options=df['categoria'].unique()
            )
        
        with col2:
            nome_filter = st.text_input("Buscar por Nome")
        
        # Aplicar filtros
        if categoria_filter:
            df = df[df['categoria'].isin(categoria_filter)]
        if nome_filter:
            df = df[df['nome'].str.contains(nome_filter, case=False)]
        
        # Exibir produtos em grade responsiva
        if st.session_state.get('mobile_view') is None:
            st.session_state.mobile_view = st.checkbox('Visualização para celular')

        # Agrupar produtos por nome
        produtos_agrupados = df.groupby('nome')
        
        # Define o número de colunas com base no tipo de visualização
        num_cols = 1 if st.session_state.mobile_view else 3
        cols = st.columns(num_cols)
        col_index = 0
        
        for nome_produto, grupo in produtos_agrupados:
            with cols[col_index % num_cols]:
                with st.container():
                    st.subheader(nome_produto)
                    
                    # Mostrar primeira imagem do grupo
                    primeira_imagem = grupo.iloc[0]['imagem_path']
                    if primeira_imagem:
                        try:
                            st.image(f"uploads/{primeira_imagem}", use_container_width=True)
                        except:
                            st.image("https://placehold.co/200x200?text=Sem+Imagem", use_container_width=True)
                    else:
                        st.image("https://placehold.co/200x200?text=Sem+Imagem", use_container_width=True)
                    
                    # Informações comuns
                    st.write(f"**Categoria:** {grupo.iloc[0]['categoria']}")
                    st.write(f"**Preço:** R$ {grupo.iloc[0]['preco_venda']:.2f}")
                    
                    # Variações por cor
                    st.write("**Variações:**")
                    for _, variacao in grupo.iterrows():
                        with st.expander(f"Cor: {variacao['cor']}"):
                            st.write(f"**Tamanho:** {variacao['tamanho']}")
                            st.write(f"**Quantidade:** {variacao['quantidade']}")
                            if variacao['quantidade'] <= 5:
                                st.warning("Estoque Baixo!")
                            if st.button(f"Excluir", key=f"del_{variacao.name}"):
                                df = df.drop(variacao.name)
                                save_data(df, "produtos")
                                st.rerun()
                    
                    st.divider()
                    
            col_index += 1
    else:
        st.info("Nenhum produto cadastrado")

with tab3:
    st.header("Controle de Estoque")
    
    df = load_data("produtos")
    if not df.empty:
        # Cálculos financeiros
        df['valor_total_custo'] = df['preco_custo'] * df['quantidade']
        df['valor_total_venda'] = df['preco_venda'] * df['quantidade']
        df['lucro_previsto'] = df['valor_total_venda'] - df['valor_total_custo']
        
        # Métricas gerais
        col1, col2, col3 = st.columns(3)
        with col1:
            total_investimento = df['valor_total_custo'].sum()
            st.metric("Total Investido", f"R$ {total_investimento:.2f}")
        with col2:
            total_previsto = df['valor_total_venda'].sum()
            st.metric("Faturamento Previsto", f"R$ {total_previsto:.2f}")
        with col3:
            lucro_total = df['lucro_previsto'].sum()
            st.metric("Lucro Previsto", f"R$ {lucro_total:.2f}")
        
        # Tabela detalhada
        st.subheader("Análise por Produto")
        df_display = df[['nome', 'quantidade', 'preco_custo', 'preco_venda', 
                        'valor_total_custo', 'valor_total_venda', 'lucro_previsto']]
        
        st.dataframe(
            df_display,
            column_config={
                "nome": "Produto",
                "quantidade": "Estoque",
                "preco_custo": st.column_config.NumberColumn("Preço Custo", format="R$ %.2f"),
                "preco_venda": st.column_config.NumberColumn("Preço Venda", format="R$ %.2f"),
                "valor_total_custo": st.column_config.NumberColumn("Total em Custo", format="R$ %.2f"),
                "valor_total_venda": st.column_config.NumberColumn("Total em Venda", format="R$ %.2f"),
                "lucro_previsto": st.column_config.NumberColumn("Lucro Previsto", format="R$ %.2f")
            },
            hide_index=True
        )
    else:
        st.info("Nenhum produto cadastrado")
