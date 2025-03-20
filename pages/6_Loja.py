import streamlit as st
import pandas as pd
from auth import check_password

st.set_page_config(
    page_title="Loja - Xible",
    page_icon="🛍️",
    layout="wide"
)

# Store styles
st.markdown("""
<style>
.store-header { 
    background: #f8f9fa;
    padding: 2rem 0;
    text-align: center;
    margin-bottom: 2rem;
}
.category-nav {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-bottom: 2rem;
}
.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 2rem;
    padding: 1rem;
}
.product-card {
    background: white;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    overflow: hidden;
    transition: transform 0.3s ease;
}
.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}
.product-image {
    width: 100%;
    height: 300px;
    object-fit: cover;
}
.product-info {
    padding: 1rem;
}
.product-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
}
.product-price {
    color: #28a745;
    font-size: 1.2rem;
    font-weight: bold;
}
.product-description {
    color: #6c757d;
    margin: 0.5rem 0;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.btn-buy {
    width: 100%;
    background: #28a745;
    color: white;
    border: none;
    padding: 0.5rem;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 1rem;
}
.modal {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    padding: 2rem;
    border-radius: 8px;
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    max-width: 90%;
    width: 500px;
}
.cart-item {
    display: flex;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #dee2e6;
}
.cart-total {
    font-size: 1.2rem;
    font-weight: bold;
    text-align: right;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'show_cart' not in st.session_state:
    st.session_state.show_cart = False
if 'show_product_details' not in st.session_state:
    st.session_state.show_product_details = None

# Load products
try:
    produtos_df = pd.read_csv("data/produtos.csv")
except Exception as e:
    st.error("Erro ao carregar produtos")
    st.stop()

# Store header
st.markdown('<div class="store-header">', unsafe_allow_html=True)
st.title("🛍️ Loja Xible")
st.markdown("Descubra nossa coleção exclusiva")
st.markdown('</div>', unsafe_allow_html=True)

# Category filter
categorias = ['Todas'] + sorted(produtos_df['categoria'].unique().tolist())
col1, col2, col3 = st.columns([1,2,1])
with col2:
    categoria = st.selectbox('Categoria', categorias, key='categoria_filter')

# Products grid
produtos_filtrados = produtos_df if categoria == 'Todas' else produtos_df[produtos_df['categoria'] == categoria]

st.markdown('<div class="product-grid">', unsafe_allow_html=True)
for idx, produto in produtos_filtrados.iterrows():
    st.markdown(f"""
    <div class="product-card">
        <img src="uploads/{produto['imagem_path']}" class="product-image" 
             onerror="this.src='https://via.placeholder.com/300x300?text=Sem+Imagem'">
        <div class="product-info">
            <div class="product-title">{produto['nome']}</div>
            <div class="product-price">R$ {produto['preco_venda']:.2f}</div>
            <div class="product-description">{produto.get('descricao', 'Sem descrição')}</div>
            <button class="btn-buy" key=f"buy_{idx}">Comprar</button>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Ver Detalhes", key=f"details_{idx}"):
        st.session_state.show_product_details = produto
    if st.button("Comprar", key=f"buy_{idx}", type="primary"):
        st.session_state.cart.append({
            'codigo': produto['codigo'],
            'nome': produto['nome'],
            'preco': produto['preco_venda'],
            'tamanho': produto['tamanho'],
            'cor': produto['cor'],
            'quantidade': 1
        })
        st.toast("✅ Produto adicionado ao carrinho!")

st.markdown('</div>', unsafe_allow_html=True)

# Cart button
if st.sidebar.button(f"🛒 Carrinho ({len(st.session_state.cart)})", use_container_width=True):
    st.session_state.show_cart = True

# Cart modal
if st.session_state.show_cart:
    with st.container():
        st.subheader("🛒 Seu Carrinho")

        if not st.session_state.cart:
            st.info("Seu carrinho está vazio")
        else:
            total = 0
            for idx, item in enumerate(st.session_state.cart):
                col1, col2, col3 = st.columns([3,2,1])
                with col1:
                    st.write(f"**{item['nome']}**")
                with col2:
                    item['quantidade'] = st.number_input("Quantidade", key=f"qty_{idx}", min_value=1, value=item['quantidade'])
                with col3:
                    if st.button("🗑️", key=f"remove_{idx}"):
                        st.session_state.cart.pop(idx)
                        st.rerun()
                total += item['preco'] * item['quantidade']

            st.write(f"**Total: R$ {total:.2f}**")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Continuar Comprando"):
                    st.session_state.show_cart = False
                    st.rerun()
            with col2:
                if st.button("Finalizar Compra", type="primary"):
                    try:
                        config_df = pd.read_csv("data/whatsapp_config.csv")
                        whatsapp_number = config_df.iloc[0]['numero']
                        mensagem = "Olá! Gostaria de fazer um pedido:\n\n"
                        for item in st.session_state.cart:
                            mensagem += f"• {item['nome']} x{item['quantidade']} = R$ {item['preco'] * item['quantidade']:.2f}\n"
                        mensagem += f"\nTotal: R$ {total:.2f}"

                        mensagem_encoded = mensagem.replace('\n', '%0A').replace(' ', '%20')
                        whatsapp_link = f"https://wa.me/+55{whatsapp_number}?text={mensagem_encoded}"

                        st.markdown(f'<a href="{whatsapp_link}" target="_blank">Enviar pedido por WhatsApp</a>', unsafe_allow_html=True)
                        st.session_state.cart = []
                        st.success("Pedido enviado! Retornando à loja...")
                        st.session_state.show_cart = False
                        st.rerun()
                    except Exception as e:
                        st.error("Erro ao processar pedido. Tente novamente.")

# Product details modal
if st.session_state.show_product_details is not None:
    produto = st.session_state.show_product_details
    with st.container():
        col1, col2 = st.columns([1,2])
        with col1:
            st.image(f"uploads/{produto['imagem_path']}", use_column_width=True)
        with col2:
            st.title(produto['nome'])
            st.write(f"**Categoria:** {produto['categoria']}")
            st.write(f"**Descrição:**\n{produto.get('descricao', '')}")
            st.write(f"**Preço:** R$ {produto['preco_venda']:.2f}")
            st.write(f"**Cor:** {produto['cor']}")
            st.write(f"**Tamanho:** {produto['tamanho']}")

            if st.button("Fechar"):
                st.session_state.show_product_details = None
                st.rerun()