import streamlit as st
import pandas as pd
from utils import load_data, save_data, validate_product_data
from auth import check_password
import time

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
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 15px;
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
</style>
""", unsafe_allow_html=True)

# Tabs para diferentes funcionalidades
tab1, tab2, tab3 = st.tabs(["📝 Cadastro", "📦 Produtos", "📊 Estoque"])

with tab1:
    st.header("Cadastro de Produto")

    with st.form("cadastro_produto", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome do Produto")
            categoria = st.selectbox("Categoria", ["Roupas", "Calçados", "Acessórios"])
            preco_custo = st.number_input("Preço de Custo", min_value=0.0, step=0.01)
            preco_venda = st.number_input("Preço de Venda", min_value=0.0, step=0.01)

        with col2:
            descricao = st.text_area("Descrição")
            imagem = st.file_uploader("Imagem do Produto", type=['jpg', 'jpeg', 'png'])

        # Variantes
        st.subheader("Variantes do Produto")
        cols = st.columns(3)
        with cols[0]:
            cor = st.text_input("Cor")
        with cols[1]:
            tamanho = st.text_input("Tamanho")
        with cols[2]:
            quantidade = st.number_input("Quantidade", min_value=0)

        if st.form_submit_button("📥 Cadastrar Produto"):
            if validate_product_data(nome, preco_custo, preco_venda, quantidade):
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

                if imagem:
                    with open(f"uploads/{imagem.name}", "wb") as f:
                        f.write(imagem.getbuffer())

                df = pd.concat([df, pd.DataFrame([novo_produto])], ignore_index=True)
                save_data(df, "produtos")
                st.success("✅ Produto cadastrado com sucesso!")

with tab2:
    st.header("Catálogo de Produtos")

    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        categoria_filter = st.multiselect("Categoria", ["Roupas", "Calçados", "Acessórios"])
    with col2:
        nome_filter = st.text_input("🔍 Buscar produto")
    with col3:
        ordenar = st.selectbox("Ordenar por", ["Nome", "Preço ↑", "Preço ↓", "Estoque"])

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
                st.markdown(f"### {nome_produto}")

                # Carrossel de imagens
                imagens = grupo['imagem_path'].unique()
                if len(imagens) > 0 and imagens[0]:
                    cols = st.columns(len(imagens))
                    for idx, img in enumerate(imagens):
                        with cols[idx]:
                            try:
                                st.image(f"uploads/{img}", use_column_width=True)
                            except:
                                st.image("https://via.placeholder.com/200x200?text=Sem+Imagem")

                # Informações do produto
                col1, col2 = st.columns([2,1])
                with col1:
                    st.write(f"**Categoria:** {grupo['categoria'].iloc[0]}")
                    st.write(f"**Descrição:** {grupo['descricao'].iloc[0]}")
                    st.write(f"**Preço:** R$ {grupo['preco_venda'].iloc[0]:.2f}")

                # Variantes agrupadas
                with col2:
                    st.write("**Variantes disponíveis:**")
                    for cor, subgrupo in grupo.groupby('cor'):
                        st.write(f"🎨 {cor}:")
                        for _, row in subgrupo.iterrows():
                            status = "inventory-low" if row['quantidade'] <= 5 else "inventory-ok"
                            st.markdown(f"""
                            <div class="variant-chip">
                                Tam: {row['tamanho']} | 
                                <span class="{status}">
                                    Estoque: {row['quantidade']}
                                </span>
                            </div>
                            """, unsafe_allow_html=True)

                st.divider()

with tab3:
    st.header("Controle de Estoque")

    df = load_data("produtos")
    if not df.empty:
        # Métricas
        total_produtos = len(df)
        produtos_baixo_estoque = len(df[df['quantidade'] <= 5])
        valor_total_estoque = (df['preco_venda'] * df['quantidade']).sum()

        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Produtos", total_produtos)
        col2.metric("Produtos em Baixa", produtos_baixo_estoque)
        col3.metric("Valor em Estoque", f"R$ {valor_total_estoque:.2f}")

        # Tabela de estoque
        st.dataframe(
            df[['nome', 'cor', 'tamanho', 'quantidade', 'preco_venda']],
            column_config={
                "nome": "Produto",
                "cor": "Cor",
                "tamanho": "Tamanho",
                "quantidade": st.column_config.NumberColumn("Estoque"),
                "preco_venda": st.column_config.NumberColumn("Preço", format="R$ %.2f")
            },
            hide_index=True
        )