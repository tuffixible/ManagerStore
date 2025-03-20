
import streamlit as st
import pandas as pd
from utils import load_data, save_data
import base64
import json
import webbrowser
import urllib.parse
import os

st.set_page_config(layout="wide")

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

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
    display: flex;
    flex-direction: column;
}

.product-card:hover {
    transform: translateY(-5px);
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
    margin: 0.5rem 0;
}

.product-description {
    font-size: 0.9rem;
    color: #666;
    margin-bottom: 1rem;
    flex-grow: 1;
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
    border: none;
    width: 100%;
    margin-top: auto;
}

.buy-button:hover {
    background-color: #ff3333;
}

.cart-badge {
    background-color: #ff4b4b;
    color: white;
    border-radius: 50%;
    padding: 0.2rem 0.5rem;
    font-size: 0.8rem;
    margin-left: 0.5rem;
}

.cart-item {
    background: white;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Load WhatsApp configuration
try:
    whatsapp_config = pd.read_csv("data/whatsapp_config.csv").iloc[0]
except:
    whatsapp_config = {'numero': '', 'mensagem_padrao': ''}

# Function to add item to cart
def add_to_cart(product):
    st.session_state.cart.append(product)
    st.success(f"{product['nome']} adicionado ao carrinho!")

# Function to send WhatsApp message
def send_whatsapp_order(items, total):
    if not whatsapp_config['numero']:
        st.error("Número do WhatsApp não configurado. Configure em Configurações.")
        return False
    
    items_text = "\n".join([f"- {item['nome']} (R$ {item['preco_venda']:.2f})" for item in items])
    message = f"Olá! Novo pedido:\n\n{items_text}\n\nTotal: R$ {total:.2f}"
    
    whatsapp_url = f"https://wa.me/{whatsapp_config['numero']}?text={urllib.parse.quote(message)}"
    webbrowser.open(whatsapp_url)
    return True

# Store tabs - reordered
store_tab, cart_tab = st.tabs(["🏪 Loja", "🛒 Carrinho"])

with cart_tab:
    if not st.session_state.cart:
        st.info("Seu carrinho está vazio")
    else:
        total = sum(item['preco_venda'] for item in st.session_state.cart)
        st.header(f"Total: R$ {total:.2f}")
        
        for item in st.session_state.cart:
            with st.container():
                st.markdown(f"""
                <div class="cart-item">
                    <h3>{item['nome']}</h3>
                    <p>R$ {item['preco_venda']:.2f}</p>
                </div>
                """, unsafe_allow_html=True)
        
        if st.button("Finalizar Compra"):
            if send_whatsapp_order(st.session_state.cart, total):
                st.session_state.cart = []
                st.success("Pedido enviado com sucesso!")
                st.rerun()

with store_tab:
    # Header
    st.markdown('<div class="store-header"><h1>🛍️ Loja Xible</h1><p>As melhores ofertas!</p></div>', unsafe_allow_html=True)

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
                produto = produtos_df.iloc[i + j].to_dict()
                with cols[j]:
                    st.markdown(f"""
                    <div class="product-card">
                        <img src="uploads/{produto['imagem_path']}" class="product-image">
                        <div class="product-title">{produto['nome']}</div>
                        <div class="product-description">{produto['descricao'][:100]}...</div>
                        <div class="product-price">R$ {produto['preco_venda']:.2f}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    # Handle missing images with st.image fallback
                    if not os.path.exists(f"uploads/{produto['imagem_path']}"):
                        st.image("https://via.placeholder.com/300", width=200)
                    if st.button("Comprar Agora", key=f"buy_{i}_{j}"):
                        add_to_cart(produto)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 3rem; padding: 2rem; background: #f5f5f5; border-radius: 10px;">
    <h3>Frete Grátis</h3>
    <p>Em compras acima de R$ 299,90 para todo o Brasil!</p>
</div>
""", unsafe_allow_html=True)
