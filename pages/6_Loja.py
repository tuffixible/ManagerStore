
import streamlit as st
import pandas as pd
from utils import load_data
import base64

st.set_page_config(layout="wide")

# Custom CSS for the store
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');

.store-header {
    text-align: center;
    padding: 2rem 0;
    background: linear-gradient(45deg, #1a1a1a, #2d2d2d);
    color: white;
    border-radius: 10px;
    margin-bottom: 2rem;
}

.product-card {
    background: white;
    border-radius: 15px;
    padding: 1rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.3s ease;
    height: 100%;
}

.product-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 6px 12px rgba(0,0,0,0.15);
}

.product-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 10px;
    margin-bottom: 1rem;
}

.product-title {
    font-family: 'Poppins', sans-serif;
    font-weight: 600;
    font-size: 1.1rem;
    margin-bottom: 0.5rem;
}

.product-price {
    font-family: 'Poppins', sans-serif;
    font-size: 1.2rem;
    color: #ff4b4b;
    font-weight: 700;
}

.product-description {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 1rem;
}

.buy-button {
    background-color: #ff4b4b;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 25px;
    text-align: center;
    cursor: pointer;
    transition: background-color 0.3s ease;
    text-decoration: none;
    display: block;
    margin-top: auto;
}

.buy-button:hover {
    background-color: #ff3333;
}

.category-filter {
    padding: 0.5rem 1rem;
    background: white;
    border-radius: 20px;
    margin: 0.5rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border: 1px solid #ddd;
}

.category-filter:hover {
    background: #f0f0f0;
}

.category-filter.active {
    background: #ff4b4b;
    color: white;
    border-color: #ff4b4b;
}

div[data-testid="stHorizontalBlock"] {
    gap: 1rem;
    padding: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="store-header"><h1>🛍️ Loja Xible</h1><p>As melhores ofertas em calçados!</p></div>', unsafe_allow_html=True)

# Load products
produtos_df = load_data("produtos")

# Filters
col1, col2 = st.columns([2,1])
with col1:
    search = st.text_input("🔍 Buscar produtos", "")
    
with col2:
    categorias = produtos_df['categoria'].unique()
    categoria_selecionada = st.selectbox("📑 Filtrar por categoria", ['Todas'] + list(categorias))

# Filter products
if search:
    produtos_df = produtos_df[produtos_df['nome'].str.contains(search, case=False)]
if categoria_selecionada != 'Todas':
    produtos_df = produtos_df[produtos_df['categoria'] == categoria_selecionada]

# Display products in grid
for i in range(0, len(produtos_df), 3):
    cols = st.columns(3)
    for j in range(3):
        if i + j < len(produtos_df):
            produto = produtos_df.iloc[i + j]
            with cols[j]:
                st.markdown(f"""
                <div class="product-card">
                    <img src="uploads/{produto['imagem_path']}" class="product-image" onerror="this.src='https://via.placeholder.com/300'">
                    <div class="product-title">{produto['nome']}</div>
                    <div class="product-description">{produto['descricao'][:100]}...</div>
                    <div class="product-price">R$ {produto['preco_venda']:.2f}</div>
                    <div style="margin-top: 1rem;">
                        <span class="category-filter">{produto['categoria']}</span>
                        <span class="category-filter">{produto['cor']}</span>
                        <span class="category-filter">Tam. {produto['tamanho']}</span>
                    </div>
                    <a href="#" class="buy-button">Comprar Agora</a>
                </div>
                """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; background: #f5f5f5; border-radius: 10px;">
    <h3>Frete Grátis</h3>
    <p>Em compras acima de R$ 299,90 para todo o Brasil!</p>
</div>
""", unsafe_allow_html=True)
