
import streamlit as st
import pandas as pd
from auth import check_password

st.set_page_config(
    page_title="Loja - Xible",
    page_icon="🛍️",
    layout="wide"
)

# Enhanced store styles
st.markdown("""
<style>
.store-container {
    padding: 2rem 0;
}
.store-header {
    background: linear-gradient(135deg, #f6f8fd 0%, #f1f4f9 100%);
    padding: 3rem 0;
    text-align: center;
    margin-bottom: 2rem;
    border-radius: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}
.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 2rem;
    padding: 1rem;
}
.product-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}
.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.12);
}
.product-image {
    width: 100%;
    height: 280px;
    object-fit: cover;
    transition: transform 0.3s ease;
}
.product-card:hover .product-image {
    transform: scale(1.05);
}
.product-info {
    padding: 1.5rem;
}
.product-title {
    font-size: 1.2rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    color: #2c3e50;
}
.product-price {
    color: #2ecc71;
    font-size: 1.3rem;
    font-weight: bold;
    margin: 0.5rem 0;
}
.product-description {
    color: #7f8c8d;
    font-size: 0.9rem;
    margin: 0.5rem 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.product-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #ecf0f1;
}
.product-size {
    background: #f8f9fa;
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    font-size: 0.9rem;
    color: #34495e;
}
.product-color {
    display: inline-block;
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    background: #f8f9fa;
    font-size: 0.9rem;
    color: #34495e;
}
.btn-buy {
    width: 100%;
    background: #2ecc71;
    color: white;
    border: none;
    padding: 0.8rem;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    transition: all 0.3s ease;
    margin-top: 1rem;
}
.btn-buy:hover {
    background: #27ae60;
    transform: translateY(-2px);
}
.category-select {
    max-width: 300px;
    margin: 0 auto 2rem auto;
}
.success-message {
    position: fixed;
    top: 20px;
    right: 20px;
    background: #2ecc71;
    color: white;
    padding: 1rem 2rem;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    z-index: 1000;
    animation: slideIn 0.3s ease-out;
}
@keyframes slideIn {
    from { transform: translateX(100%); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Load products
try:
    produtos_df = pd.read_csv("data/produtos.csv")
except Exception as e:
    st.error("Erro ao carregar produtos")
    st.stop()

# Store header
st.markdown('<div class="store-header">', unsafe_allow_html=True)
st.title("🛍️ Loja Xible")
st.markdown("### Descubra nossa coleção exclusiva de calçados")
st.markdown('</div>', unsafe_allow_html=True)

# Category filter with centered layout
col1, col2, col3 = st.columns([1,2,1])
with col2:
    categorias = ['Todas'] + sorted(produtos_df['categoria'].unique().tolist())
    categoria = st.selectbox('Filtrar por categoria:', categorias, key='categoria_filter')

# Filter products
produtos_filtrados = produtos_df if categoria == 'Todas' else produtos_df[produtos_df['categoria'] == categoria]

# Products grid
st.markdown('<div class="product-grid">', unsafe_allow_html=True)
for idx, produto in produtos_filtrados.iterrows():
    st.markdown(f"""
    <div class="product-card">
        <img src="uploads/{produto['imagem_path']}" class="product-image" 
             onerror="this.src='https://via.placeholder.com/300x300?text=Imagem+Indisponível'">
        <div class="product-info">
            <div class="product-title">{produto['nome']}</div>
            <div class="product-price">R$ {produto['preco_venda']:.2f}</div>
            <div class="product-description">{produto.get('descricao', 'Descrição não disponível')}</div>
            <div class="product-meta">
                <span class="product-size">Tamanho: {produto['tamanho']}</span>
                <span class="product-color">{produto['cor']}</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Buttons for product actions
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📝 Detalhes", key=f"details_{idx}"):
            st.session_state.show_product_details = produto
    with col2:
        if st.button("🛒 Comprar", key=f"buy_{idx}", type="primary"):
            st.session_state.cart.append({
                'codigo': produto['codigo'],
                'nome': produto['nome'],
                'preco': produto['preco_venda'],
                'tamanho': produto['tamanho'],
                'cor': produto['cor'],
                'quantidade': 1
            })
            st.toast(f"✅ {produto['nome']} adicionado ao carrinho!")

st.markdown('</div>', unsafe_allow_html=True)

# Product details modal
if hasattr(st.session_state, 'show_product_details') and st.session_state.show_product_details is not None:
    produto = st.session_state.show_product_details
    with st.container():
        col1, col2 = st.columns([1,2])
        with col1:
            st.image(f"uploads/{produto['imagem_path']}", use_column_width=True)
        with col2:
            st.title(produto['nome'])
            st.write(f"**Categoria:** {produto['categoria']}")
            st.write(f"**Descrição:**\n{produto.get('descricao', 'Descrição não disponível')}")
            st.write(f"**Preço:** R$ {produto['preco_venda']:.2f}")
            st.write(f"**Cor:** {produto['cor']}")
            st.write(f"**Tamanho:** {produto['tamanho']}")
            
            if st.button("Fechar detalhes"):
                st.session_state.show_product_details = None
                st.rerun()

# Floating cart button with counter
cart_count = len(st.session_state.cart)
st.sidebar.markdown(f"""
<div style="position: fixed; bottom: 20px; right: 20px; z-index: 1000;">
    <button style="background: #2ecc71; color: white; border: none; padding: 15px 30px; 
                   border-radius: 25px; font-size: 16px; cursor: pointer; display: flex; 
                   align-items: center; gap: 10px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
        🛒 Carrinho ({cart_count})
    </button>
</div>
""", unsafe_allow_html=True)

