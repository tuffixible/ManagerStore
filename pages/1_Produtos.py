import streamlit as st
import pandas as pd
from utils import load_data, save_data, validate_product_data
from auth import check_password

if not check_password():
    st.stop()

st.title("🛍️ Gestão de Produtos")

# Custom CSS for better styling
st.markdown("""
<style>
.product-card {
    background: white;
    border-radius: 10px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    transition: transform 0.2s;
}
.product-card:hover {
    transform: translateY(-5px);
}
.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    padding: 20px 0;
}
.product-image {
    width: 100%;
    height: 250px;
    object-fit: contain;
    border-radius: 8px;
    margin-bottom: 15px;
    max-height: 300px;
}
.variant-chip {
    display: inline-block;
    padding: 5px 10px;
    margin: 2px;
    border-radius: 15px;
    font-size: 12px;
    background: #f0f2f6;
}
.inventory-low {
    color: #ff4b4b;
    font-weight: bold;
}
.inventory-ok {
    color: #00c853;
}
.variant-form {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}
.flying-bird {
    position: fixed;
    font-size: 24px;
    z-index: 1000;
    transform-origin: center;
    animation: fly 15s linear infinite, flap 0.5s ease-in-out infinite;
    cursor: pointer;
    text-shadow: 0 0 5px rgba(255,255,255,0.8);
}
@keyframes fly {
    0% { left: -50px; top: 100px; transform: scaleX(1); }
    25% { left: 40%; top: 80%; transform: scaleX(1); }
    26% { transform: scaleX(-1); }
    50% { left: 95%; top: 30%; transform: scaleX(-1); }
    51% { transform: scaleX(1); }
    75% { left: 40%; top: 20%; transform: scaleX(1); }
    100% { left: -50px; top: 100px; transform: scaleX(1); }
}
@keyframes flap {
    0%, 100% { transform: translateY(0) rotate(5deg); }
    50% { transform: translateY(-5px) rotate(-5deg); }
}
.product-image {
    transition: all 0.3s ease;
    border: 3px solid transparent;
}
.product-image:hover {
    transform: scale(1.25);
    z-index: 100;
    box-shadow: 0 0 20px var(--product-color, rgba(255,255,255,0.5));
    border-color: var(--product-color, #fff);
}
</style>
""", unsafe_allow_html=True)

# Tabs para diferentes funcionalidades
tab1, tab2, tab3 = st.tabs(["📝 Cadastro", "📦 Produtos", "📊 Estoque"])

with tab1:
    st.header("Cadastro de Produto")

    with st.form("cadastro_produto", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("📋 Nome do Produto")
            categoria = st.selectbox("🏷️ Categoria", ["Roupas", "Calçados", "Acessórios"])
            preco_custo = st.number_input("💰 Preço de Custo", min_value=0.0, step=0.01)
            preco_venda = st.number_input("💵 Preço de Venda", min_value=0.0, step=0.01)

        with col2:
            descricao = st.text_area("📝 Descrição")
            imagem = st.file_uploader("🖼️ Imagem do Produto", type=['jpg', 'jpeg', 'png'])

        st.markdown("---")
        st.subheader("🎨 Variantes do Produto")

        if 'variantes' not in st.session_state:
            st.session_state.variantes = [{"cor": "", "tamanho": "", "quantidade": 0}]

        variantes = []
        for i, variante in enumerate(st.session_state.variantes):
            with st.container():
                st.markdown(f"""
                <div style='
                    background: white;
                    padding: 10px;
                    border-radius: 8px;
                    margin: 5px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                '>""", unsafe_allow_html=True)
                cols = st.columns([1,1,1])
                with cols[0]:
                    cor = st.text_input("Cor", value=variante["cor"], key=f"form_cor_{i}", placeholder="Digite a cor")
                with cols[1]:
                    tamanho = st.text_input("Tamanho", value=variante["tamanho"], key=f"form_tamanho_{i}", placeholder="Digite o tamanho")
                with cols[2]:
                    quantidade = st.number_input("Quantidade", value=variante["quantidade"], min_value=0, key=f"form_qtd_{i}")
                st.markdown("</div>", unsafe_allow_html=True)
                variantes.append({"cor": cor, "tamanho": tamanho, "quantidade": quantidade})

        submit = st.form_submit_button("📥 Cadastrar Produto")

    # Add variant button outside the form
    if st.button("➕ Adicionar Variante", key="add_variant_btn"):
        st.session_state.variantes.append({"cor": "", "tamanho": "", "quantidade": 0})
        st.rerun()

    if submit:
            if validate_product_data(nome, preco_custo, preco_venda, 0):
                df = load_data("produtos")
                for variante in variantes:
                    if variante["cor"] or variante["tamanho"]:  # Only add non-empty variants
                        novo_produto = {
                            'codigo': len(df) + 1,
                            'nome': nome,
                            'categoria': categoria,
                            'cor': variante['cor'],
                            'tamanho': variante['tamanho'],
                            'descricao': descricao,
                            'preco_custo': preco_custo,
                            'preco_venda': preco_venda,
                            'quantidade': variante['quantidade'],
                            'imagem_path': imagem.name if imagem else ''
                        }
                        if imagem:
                            with open(f"uploads/{imagem.name}", "wb") as f:
                                f.write(imagem.getbuffer())
                        df = pd.concat([df, pd.DataFrame([novo_produto])], ignore_index=True)
                save_data(df, "produtos")
                st.session_state.variantes = [{"cor": "", "tamanho": "", "quantidade": 0}]
                st.success("✅ Produto e variantes cadastrados com sucesso!")
                st.rerun()

with tab2:
    st.header("Catálogo de Produtos")

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        categoria_filter = st.multiselect("🏷️ Categoria", ["Roupas", "Calçados", "Acessórios"])
    with col2:
        nome_filter = st.text_input("🔍 Buscar produto")
    with col3:
        ordenar = st.selectbox("📊 Ordenar por", ["Nome", "Preço ↑", "Preço ↓", "Estoque"])

    df = load_data("produtos")

    if not df.empty:
        # Aplicar filtros
        if categoria_filter:
            df = df[df['categoria'].isin(categoria_filter)]
        if nome_filter:
            df = df[df['nome'].str.contains(nome_filter, case=False)]

        # Agrupar produtos por nome
        produtos_agrupados = df.groupby('nome')

        for nome_produto, grupo in produtos_agrupados:
            with st.container():
                col1, col2 = st.columns([0.9, 0.1])
                with col1:
                    st.markdown(f"## {nome_produto}")
                with col2:
                    cor_titulo = st.color_picker("", "#000000", key=f"color_{nome_produto}")

                # Botão de exclusão
                col_del1, col_del2 = st.columns([3,1])
                with col_del2:
                    delete_key = f"del_{nome_produto}"
                    if delete_key not in st.session_state:
                        st.session_state[delete_key] = False

                    if st.button(f"🗑️ Excluir", key=f"btn_{delete_key}"):
                        st.session_state[delete_key] = True

                    if st.session_state[delete_key]:
                        if st.button("❌ Confirmar exclusão?", key=f"confirm_{delete_key}"):
                            df = df[df['nome'] != nome_produto]
                            save_data(df, "produtos")
                            st.success(f"✅ Produto {nome_produto} excluído com sucesso!")
                            st.rerun()
                        if st.button("↩️ Cancelar", key=f"cancel_{delete_key}"):
                            st.session_state[delete_key] = False
                            st.rerun()

                # Container mais compacto para cada produto
                st.markdown(f"""
                <div style='
                    background: linear-gradient(145deg, #ffffff, #f0f0f0);
                    padding: 15px;
                    border-radius: 10px;
                    margin: 10px 0;
                    box-shadow: 5px 5px 10px #d1d1d1;
                    position: relative;
                '>
                    <h3 style='
                        color: {cor_titulo};
                        font-size: 20px;
                        margin-bottom: 10px;
                        text-transform: uppercase;
                    '>{nome_produto}</h3>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('<div class="product-card">', unsafe_allow_html=True)

                # Imagens em tamanho reduzido
                imagens = grupo['imagem_path'].unique()
                if len(imagens) > 0 and imagens[0]:
                    cols = st.columns(min(len(imagens), 3))
                    for idx, img in enumerate(imagens[:3]):
                        with cols[idx]:
                            try:
                                try:
                                    st.image(f"uploads/{img}", width=120)
                                except Exception:
                                    st.image("https://via.placeholder.com/120x120?text=Sem+Imagem", width=120)
                            except:
                                st.image("https://via.placeholder.com/120x120?text=Sem+Imagem")

                # Informações do produto em layout compacto
                col1, col2 = st.columns([3,2])
                with col1:
                    st.write(f"**🏷️ Categoria:** {grupo['categoria'].iloc[0]}")
                    st.write(f"**📝 Descrição:** {grupo['descricao'].iloc[0]}")
                    st.write(f"**💰 Preço:** R$ {grupo['preco_venda'].iloc[0]:.2f}")

                # Variantes agrupadas
                with col2:
                    st.write("**🎨 Variantes disponíveis:**")
                    for cor, subgrupo in grupo.groupby('cor'):
                        st.write(f"🎨 {cor}:")
                        for _, row in subgrupo.iterrows():
                            status = "inventory-low" if row['quantidade'] <= 5 else "inventory-ok"
                            st.markdown(f"""
                            <div class="variant-chip">
                                📏 Tam: {row['tamanho']} | 
                                <span class="{status}">
                                    📦 Estoque: {row['quantidade']}
                                </span>
                            </div>
                            """, unsafe_allow_html=True)

                st.markdown('</div>', unsafe_allow_html=True)
                st.divider()

with tab3:
    st.header("📊 Controle de Estoque")

    df = load_data("produtos")
    if not df.empty:
        # Calcular valores totais
        total_estoque = df['quantidade'].sum()
        produtos_baixo_estoque = len(df[df['quantidade'] <= 5])
        valor_total_estoque = (df['preco_venda'] * df['quantidade']).sum()
        custo_total_estoque = (df['preco_custo'] * df['quantidade']).sum()
        margem_total = valor_total_estoque - custo_total_estoque

        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("📦 Total em Estoque", total_estoque)
        col2.metric("⚠️ Produtos em Baixa", produtos_baixo_estoque)
        col3.metric("💰 Valor Total Venda", f"R$ {valor_total_estoque:.2f}")
        col4.metric("💵 Custo Total", f"R$ {custo_total_estoque:.2f}")
        col5.metric("📈 Margem Total", f"R$ {margem_total:.2f}")

        # Tabela de estoque estilizada
        st.markdown("""
        <style>
        .stDataFrame {
            background: white;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        </style>
        """, unsafe_allow_html=True)

        # Seleção de produtos para ações
        selected = st.multiselect(
            "Selecione produtos para gerenciar",
            df['nome'].unique(),
            key="stock_select"
        )

        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Excluir Selecionados") and selected:
                if st.button("Confirmar exclusão?"):
                    df = df[~df['nome'].isin(selected)]
                    save_data(df, "produtos")
                    st.success("✅ Produtos excluídos com sucesso!")
                    st.rerun()

        with col2:
            if st.button("✏️ Editar Selecionados") and selected:
                st.session_state.editing = True

        # Tabela editável se estiver no modo de edição
        if hasattr(st.session_state, 'editing') and st.session_state.editing and selected:
            edited_df = st.data_editor(
                df[df['nome'].isin(selected)],
                column_config={
                    "nome": "📦 Produto",
                    "cor": "🎨 Cor",
                    "tamanho": "📏 Tamanho",
                    "quantidade": st.column_config.NumberColumn("📊 Estoque"),
                    "preco_custo": st.column_config.NumberColumn("💰 Preço Custo", format="R$ %.2f"),
                    "preco_venda": st.column_config.NumberColumn("💰 Preço Venda", format="R$ %.2f")
                },
                hide_index=True,
                key="edit_table"
            )

            if st.button("💾 Salvar Alterações"):
                # Atualizar o DataFrame original com as alterações
                df.update(edited_df)
                save_data(df, "produtos")
                st.success("✅ Alterações salvas com sucesso!")
                st.session_state.editing = False
                st.rerun()
        else:
            # Exibir tabela normal
            st.dataframe(
                df[['nome', 'cor', 'tamanho', 'quantidade', 'preco_custo', 'preco_venda']],
                column_config={
                    "nome": "📦 Produto",
                    "cor": "🎨 Cor",
                    "tamanho": "📏 Tamanho",
                    "quantidade": st.column_config.NumberColumn("📊 Estoque"),
                    "preco_custo": st.column_config.NumberColumn("💰 Preço Custo", format="R$ %.2f"),
                    "preco_venda": st.column_config.NumberColumn("💰 Preço Venda", format="R$ %.2f")
                },
                hide_index=True
            )

if __name__ == "__main__":
    st.stop()