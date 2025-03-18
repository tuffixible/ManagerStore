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
    
    # Inicializar state para variantes
    if 'variants' not in st.session_state:
        st.session_state.variants = [{"cor": "", "tamanho": "", "quantidade": 0}]

    with st.form("cadastro_produto"):
        nome = st.text_input("Nome do Produto", key="nome_produto")
        categoria = st.selectbox(
            "Categoria",
            ["Roupas", "Calçados", "Acessórios"],
            key="categoria_produto"
        )
        preco_custo = st.number_input("Preço de Custo", min_value=0.0, step=0.01, key="preco_custo")
        preco_venda = st.number_input("Preço de Venda", min_value=0.0, step=0.01, key="preco_venda")
        descricao = st.text_area("Descrição", key="descricao_produto")
        imagem = st.file_uploader("Imagem do Produto", type=['jpg', 'jpeg', 'png'], key="imagem_produto")

        st.subheader("Variantes do Produto")
        for i, variant in enumerate(st.session_state.variants):
            col1, col2, col3 = st.columns(3)
            with col1:
                st.session_state.variants[i]["cor"] = st.text_input("Cor", key=f"cor_{i}", value=variant["cor"])
            with col2:
                st.session_state.variants[i]["tamanho"] = st.text_input("Tamanho", key=f"tamanho_{i}", value=variant["tamanho"])
            with col3:
                st.session_state.variants[i]["quantidade"] = st.number_input("Quantidade", key=f"qtd_{i}", min_value=0, step=1, value=variant["quantidade"])
        # Remove this section since it's duplicated and causing errors
            st.error("Erro na visualização mobile")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.form_submit_button("+ Adicionar Variante"):
                st.session_state.variants.append({"cor": "", "tamanho": "", "quantidade": 0})
                st.rerun()
        with col2:
            if st.form_submit_button("- Remover Última Variante") and len(st.session_state.variants) > 1:
                st.session_state.variants.pop()
                st.rerun()

        submitted = st.form_submit_button("Cadastrar Produto")
        
        if submitted:
            if validate_product_data(nome, preco_custo, preco_venda, 0):
                # Salvar imagem se existir
                if imagem:
                    with open(f"uploads/{imagem.name}", "wb") as f:
                        f.write(imagem.getbuffer())
                df = load_data("produtos")
                
                # Criar uma lista de produtos com todas as variantes
                novos_produtos = []
                for variant in st.session_state.variants:
                    novo_produto = {
                        'codigo': len(df) + len(novos_produtos) + 1,
                        'nome': nome,
                        'categoria': categoria,
                        'cor': variant['cor'],
                        'tamanho': variant['tamanho'],
                        'descricao': descricao,
                        'preco_custo': preco_custo,
                        'preco_venda': preco_venda,
                        'quantidade': variant['quantidade'],
                        'imagem_path': imagem.name if imagem else ''
                    }
                    novos_produtos.append(novo_produto)
                
                df = pd.concat([df, pd.DataFrame(novos_produtos)], ignore_index=True)
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

        import time
        if 'image_index' not in st.session_state:
            st.session_state.image_index = {}
            st.session_state.last_update = {}

        # Agrupar produtos por nome e cor
        produtos_agrupados = df.groupby(['nome', 'cor'])
        
        # Agrupar primeiro por nome do produto
        produtos_por_nome = df.groupby('nome')
        
        # Define o número de colunas com base no tipo de visualização
        num_cols = 1 if st.session_state.mobile_view else 3
        cols = st.columns(num_cols)
        col_index = 0
        
        for nome_produto, grupo_produto in produtos_por_nome:
            # Agrupar as variantes por cor
            variantes_por_cor = grupo_produto.groupby('cor')
            with cols[col_index % num_cols]:
                with st.container():
                    st.subheader(nome_produto)
                    primeira_variante = grupo_produto.iloc[0]
                    
                    # Gerenciar carrossel de imagens
                    produto_key = f"{nome_produto}"
                    
                    # Inicializar variáveis de estado para o produto
                    if produto_key not in st.session_state.image_index:
                        st.session_state.image_index[produto_key] = 0
                        st.session_state.last_update[produto_key] = time.time()
                    
                    # Obter todas as imagens únicas do produto
                    todas_imagens = grupo_produto['imagem_path'].unique().tolist()
                    if todas_imagens:
                        # Atualizar índice da imagem a cada 5 segundos
                        current_time = time.time()
                        if current_time - st.session_state.last_update[produto_key] >= 5:
                            st.session_state.image_index[produto_key] = (st.session_state.image_index[produto_key] + 1) % len(todas_imagens)
                            st.session_state.last_update[produto_key] = current_time
                        
                        # Mostrar imagem atual
                        imagem_atual = todas_imagens[st.session_state.image_index[produto_key]]
                        if imagem_atual:
                            try:
                                st.image(f"uploads/{imagem_atual}", use_container_width=True)
                            except:
                                st.image("https://placehold.co/200x200?text=Sem+Imagem", use_container_width=True)
                    else:
                        st.image("https://placehold.co/200x200?text=Sem+Imagem", use_container_width=True)
                    
                    # Informações comuns
                    st.write(f"**Categoria:** {primeira_variante['categoria']}")
                    st.write(f"**Preço:** R$ {primeira_variante['preco_venda']:.2f}")
                    
                    # Exibir variantes agrupadas por cor com sistema de vendas
                    with st.expander("Ver todas as variantes"):
                        for cor, variantes_cor in variantes_por_cor:
                            st.subheader(f"Cor: {cor}", divider="gray")
                            
                            # Criar tabela de variantes
                            data = []
                            for _, variante in variantes_cor.iterrows():
                                data.append({
                                    "Tamanho": variante['tamanho'],
                                    "Quantidade": variante['quantidade'],
                                    "Preço": f"R$ {variante['preco_venda']:.2f}",
                                    "Status": "⚠️ Baixo!" if variante['quantidade'] <= 5 else "✅ OK",
                                    "Ações": {
                                        "variante_id": variante.name,
                                        "quantidade": variante['quantidade'],
                                        "preco": variante['preco_venda']
                                    }
                                })
                            
                            # Criar DataFrame para a tabela
                            df_display = pd.DataFrame(data)
                            
                            # Configurar colunas para o editor
                            column_config = {
                                "Tamanho": st.column_config.TextColumn("Tamanho", width="medium"),
                                "Quantidade": st.column_config.NumberColumn("Quantidade", width="small"),
                                "Preço": st.column_config.TextColumn("Preço", width="small"),
                                "Status": st.column_config.TextColumn("Status", width="small"),
                                "Selecionar": st.column_config.CheckboxColumn(
                                    "Selecionar",
                                    default=False,
                                    help="Selecione para vender"
                                )
                            }
                            
                            # Adicionar coluna de seleção
                            df_display['Selecionar'] = False
                            df_display['variante_id'] = [d['Ações']['variante_id'] for d in data]
                            df_display['preco_venda'] = [d['Ações']['preco'] for d in data]
                            
                            # Exibir tabela com editor
                            edited_df = st.data_editor(
                                df_display[['Tamanho', 'Quantidade', 'Preço', 'Status', 'Selecionar']],
                                column_config=column_config,
                                hide_index=True,
                                key=f"table_{cor}_{nome_produto}"
                            )
                            
                            # Filtrar linhas selecionadas
                            selected_rows = edited_df[edited_df['Selecionar']]
                            
                            if not selected_rows.empty:
                                with st.form(key=f"venda_form_{cor}_{nome_produto}"):
                                    st.subheader("Realizar Venda", divider="green")
                                    
                                    total_venda = 0
                                    for idx, row in selected_rows.iterrows():
                                        variante_idx = df_display.index[idx]
                                        qtd_disponivel = df_display.loc[variante_idx, 'Quantidade']
                                        preco = float(df_display.loc[variante_idx, 'preco_venda'])
                                        
                                        col1, col2 = st.columns(2)
                                        with col1:
                                            st.text(f"Tamanho: {row['Tamanho']}")
                                        with col2:
                                            qtd_venda = st.number_input(
                                                "Quantidade",
                                                min_value=1,
                                                max_value=qtd_disponivel,
                                                value=1,
                                                key=f"qtd_{idx}"
                                            )
                                        
                                        total_venda += qtd_venda * preco
                                    
                                    st.metric("Total da Venda", f"R$ {total_venda:.2f}")
                                    
                                    if st.form_submit_button("Confirmar Venda", type="primary"):
                                        # Atualizar estoque
                                        for idx, row in selected_rows.iterrows():
                                            if row['Ações']:
                                                variante_id = row['Ações']['variante_id']
                                                qtd_venda = st.session_state[f"qtd_{variante_id}"]
                                                
                                                # Atualizar DataFrame
                                                df.loc[variante_id, 'quantidade'] -= qtd_venda
                                        
                                        # Salvar alterações
                                        save_data(df, "produtos")
                                        st.success("Venda realizada com sucesso!")
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
