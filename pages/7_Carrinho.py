
import streamlit as st
import pandas as pd
import json
from auth import check_password

if not check_password():
    st.stop()

st.set_page_config(page_title="Carrinho - Xible", page_icon="🛒", layout="wide")

# Estilo do carrinho
st.markdown("""
<style>
.cart-item {
    background: white;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}
.cart-total {
    font-size: 24px;
    font-weight: bold;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 10px;
    margin: 20px 0;
}
.whatsapp-button {
    background-color: #25D366;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    display: inline-block;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🛒 Carrinho de Compras")

# JavaScript para carregar o carrinho
st.markdown("""
<script>
const cartItems = JSON.parse(localStorage.getItem('cart') || '[]');
window.parent.postMessage({type: 'cart_data', data: cartItems}, '*');

function removeItem(index) {
    let cart = JSON.parse(localStorage.getItem('cart') || '[]');
    cart.splice(index, 1);
    localStorage.setItem('cart', JSON.stringify(cart));
    window.location.reload();
}

function updateQuantity(index, delta) {
    let cart = JSON.parse(localStorage.getItem('cart') || '[]');
    cart[index].quantidade = Math.max(1, cart[index].quantidade + delta);
    localStorage.setItem('cart', JSON.stringify(cart));
    window.location.reload();
}
</script>
""", unsafe_allow_html=True)

# Placeholder para os itens do carrinho
if 'cart_items' not in st.session_state:
    st.session_state.cart_items = []

# Exibir itens do carrinho
total = 0
for idx, item in enumerate(st.session_state.cart_items):
    with st.container():
        st.markdown(f"""
        <div class="cart-item">
            <h3>{item['nome']}</h3>
            <p>Tamanho: {item['tamanho']} | Cor: {item['cor']}</p>
            <p>Preço: R$ {item['preco']:.2f} x {item['quantidade']} = R$ {item['preco'] * item['quantidade']:.2f}</p>
            <button onclick="updateQuantity({idx}, -1)">-</button>
            <span>{item['quantidade']}</span>
            <button onclick="updateQuantity({idx}, 1)">+</button>
            <button onclick="removeItem({idx})">Remover</button>
        </div>
        """, unsafe_allow_html=True)
        total += item['preco'] * item['quantidade']

if st.session_state.cart_items:
    st.markdown(f"""
    <div class="cart-total">
        Total: R$ {total:.2f}
    </div>
    """, unsafe_allow_html=True)
    
    # Botão para finalizar compra via WhatsApp
    vendedores = pd.read_csv("data/usuarios.csv")
    vendedores = vendedores[vendedores['perfil'] == 'vendedor']
    vendedor = st.selectbox("Escolha um vendedor:", vendedores['usuario'])
    
    if st.button("Finalizar Compra"):
        mensagem = "Olá! Gostaria de fazer um pedido:\n\n"
        for item in st.session_state.cart_items:
            mensagem += f"- {item['nome']} ({item['cor']}, Tam: {item['tamanho']})\n"
            mensagem += f"  Quantidade: {item['quantidade']} x R$ {item['preco']:.2f} = R$ {item['preco'] * item['quantidade']:.2f}\n"
        mensagem += f"\nTotal: R$ {total:.2f}"
        
        mensagem_encoded = mensagem.replace('\n', '%0A').replace(' ', '%20')
        whatsapp_link = f"https://wa.me/+55{vendedores[vendedores['usuario'] == vendedor]['telefone'].iloc[0]}?text={mensagem_encoded}"
        
        st.markdown(f'<a href="{whatsapp_link}" target="_blank" class="whatsapp-button">Enviar pedido por WhatsApp</a>', unsafe_allow_html=True)
else:
    st.info("Seu carrinho está vazio")
