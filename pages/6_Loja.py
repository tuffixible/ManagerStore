
import streamlit as st
import pandas as pd
from auth import check_password

# Configuração da página
st.set_page_config(
    page_title="Loja - Xible",
    page_icon="🛍️",
    layout="wide"
)

# Estilo da loja
st.markdown("""
<style>
.product-card {
    background: white;
    border-radius: 10px;
    padding: 15px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
    transition: transform 0.3s;
}
.product-card:hover {
    transform: translateY(-5px);
}
.product-image {
    width: 100%;
    border-radius: 8px;
    margin-bottom: 10px;
}
.price {
    font-size: 24px;
    color: #2ecc71;
    font-weight: bold;
}
.category-tag {
    background: #f0f2f6;
    padding: 5px 10px;
    border-radius: 15px;
    font-size: 12px;
    color: #666;
}
.buy-button {
    background-color: #2ecc71;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    text-align: center;
    cursor: pointer;
    width: 100%;
    margin-top: 10px;
    border: none;
}
.buy-button:hover {
    background-color: #27ae60;
}
</style>
""", unsafe_allow_html=True)

# Carregar produtos
produtos_df = pd.read_csv("data/produtos.csv")

# Sidebar com filtros
st.sidebar.title("Filtros")
categorias = ['Todos'] + list(produtos_df['categoria'].unique())
categoria_selecionada = st.sidebar.selectbox('Categoria', categorias)

preco_min, preco_max = st.sidebar.slider(
    'Faixa de Preço',
    float(produtos_df['preco_venda'].min()),
    float(produtos_df['preco_venda'].max()),
    (float(produtos_df['preco_venda'].min()), float(produtos_df['preco_venda'].max()))
)

# Filtrar produtos
if categoria_selecionada != 'Todos':
    produtos_filtrados = produtos_df[produtos_df['categoria'] == categoria_selecionada]
else:
    produtos_filtrados = produtos_df

produtos_filtrados = produtos_filtrados[
    (produtos_filtrados['preco_venda'] >= preco_min) &
    (produtos_filtrados['preco_venda'] <= preco_max)
]

# Header da loja
st.title("🛍️ Loja Xible")
st.markdown("### Encontre os melhores produtos aqui!")

# Grid de produtos
cols = st.columns(3)
for idx, produto in produtos_filtrados.iterrows():
    with cols[idx % 3]:
        st.markdown(f"""
        <div class="product-card">
            <img src="{produto.get('imagem', 'default.jpg')}" class="product-image">
            <span class="category-tag">{produto['categoria']}</span>
            <h3>{produto['nome']}</h3>
            <p>{produto.get('descricao', '')}</p>
            <div class="price">R$ {produto['preco']:.2f}</div>
            <button class="buy-button">Comprar</button>
        </div>
        """, unsafe_allow_html=True)
