
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
.product-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    padding: 20px 0;
}
.product-card {
    background: white;
    border-radius: 10px;
    padding: 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.product-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 5px 20px rgba(0,0,0,0.2);
}
.product-image-container {
    position: relative;
    padding-top: 100%;
    overflow: hidden;
}
.product-image {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;
}
.product-card:hover .product-image {
    transform: scale(1.1);
}
.product-info {
    padding: 15px;
    text-align: center;
}
.product-name {
    font-size: 1.1em;
    font-weight: 600;
    margin: 10px 0;
    color: #333;
}
.product-price {
    font-size: 1.2em;
    color: #2ecc71;
    font-weight: bold;
    margin: 10px 0;
}
.product-buttons {
    display: flex;
    gap: 10px;
    justify-content: center;
    margin-top: 15px;
}
.btn {
    padding: 8px 15px;
    border-radius: 5px;
    border: none;
    cursor: pointer;
    transition: all 0.3s ease;
    font-weight: 500;
}
.btn-primary {
    background-color: #2ecc71;
    color: white;
}
.btn-secondary {
    background-color: #f8f9fa;
    color: #333;
    border: 1px solid #ddd;
}
.btn:hover {
    opacity: 0.9;
    transform: translateY(-2px);
}
.modal {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.8);
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
}
.modal-content {
    background: white;
    padding: 30px;
    border-radius: 10px;
    max-width: 800px;
    width: 90%;
    max-height: 90vh;
    overflow-y: auto;
    position: relative;
}
.cart-summary {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-top: 20px;
}
.cart-item {
    display: flex;
    align-items: center;
    padding: 15px;
    border-bottom: 1px solid #eee;
}
.cart-item-info {
    flex-grow: 1;
    padding: 0 15px;
}
.cart-item-actions {
    display: flex;
    align-items: center;
    gap: 10px;
}
.cart-total {
    font-size: 1.2em;
    font-weight: bold;
    text-align: right;
    padding: 20px;
}
.category-filter {
    background: white;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Inicializar estados da sessão
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'show_cart' not in st.session_state:
    st.session_state.show_cart = False
if 'show_product_details' not in st.session_state:
    st.session_state.show_product_details = None

# Carregar produtos
produtos_df = pd.read_csv("data/produtos.csv")

# Sidebar com filtros
with st.sidebar:
    st.markdown("### 🔍 Filtros")
    
    # Filtro de categoria
    categorias = ['Todas'] + sorted(produtos_df['categoria'].unique().tolist())
    categoria_selecionada = st.selectbox('Categoria', categorias)
    
    # Filtro de preço
    preco_min, preco_max = st.slider(
        'Faixa de Preço',
        float(produtos_df['preco_venda'].min()),
        float(produtos_df['preco_venda'].max()),
        (float(produtos_df['preco_venda'].min()), float(produtos_df['preco_venda'].max()))
    )

# Aplicar filtros
produtos_filtrados = produtos_df.copy()
if categoria_selecionada != 'Todas':
    produtos_filtrados = produtos_filtrados[produtos_filtrados['categoria'] == categoria_selecionada]
produtos_filtrados = produtos_filtrados[
    (produtos_filtrados['preco_venda'] >= preco_min) &
    (produtos_filtrados['preco_venda'] <= preco_max)
]

# Header da loja
col1, col2 = st.columns([4,1])
with col1:
    st.title("🛍️ Loja Xible")
with col2:
    if st.button(f"🛒 Carrinho ({len(st.session_state.cart)})", use_container_width=True):
        st.session_state.show_cart = True

# Mostrar carrinho
if st.session_state.show_cart:
    st.markdown("## 🛒 Seu Carrinho")
    
    if not st.session_state.cart:
        st.info("Seu carrinho está vazio")
        if st.button("Continuar Comprando"):
            st.session_state.show_cart = False
            st.rerun()
    else:
        total = 0
        for idx, item in enumerate(st.session_state.cart):
            with st.container():
                col1, col2, col3 = st.columns([3,2,1])
                with col1:
                    st.markdown(f"**{item['nome']}**")
                    st.text(f"Tamanho: {item['tamanho']} | Cor: {item['cor']}")
                with col2:
                    qty_col1, qty_col2, qty_col3 = st.columns([1,1,1])
                    with qty_col1:
                        if st.button("-", key=f"minus_{idx}"):
                            if item['quantidade'] > 1:
                                st.session_state.cart[idx]['quantidade'] -= 1
                                st.rerun()
                    with qty_col2:
                        st.write(f"{item['quantidade']}")
                    with qty_col3:
                        if st.button("+", key=f"plus_{idx}"):
                            st.session_state.cart[idx]['quantidade'] += 1
                            st.rerun()
                with col3:
                    st.write(f"R$ {item['preco'] * item['quantidade']:.2f}")
                    if st.button("🗑️", key=f"remove_{idx}"):
                        st.session_state.cart.pop(idx)
                        st.rerun()
                
                total += item['preco'] * item['quantidade']
        
        st.markdown(f"### Total: R$ {total:.2f}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Continuar Comprando", use_container_width=True):
                st.session_state.show_cart = False
                st.rerun()
        with col2:
            if st.button("Finalizar Compra", type="primary", use_container_width=True):
                # Preparar mensagem para WhatsApp
                itens = "\n".join([
                    f"• {item['nome']} ({item['cor']}, {item['tamanho']}) x{item['quantidade']} = R$ {item['preco'] * item['quantidade']:.2f}"
                    for item in st.session_state.cart
                ])
                mensagem = f"Olá! Gostaria de fazer um pedido:\n\n{itens}\n\nTotal: R$ {total:.2f}"
                mensagem_encoded = mensagem.replace('\n', '%0A').replace(' ', '%20')
                
                try:
                    config_df = pd.read_csv("data/whatsapp_config.csv")
                    whatsapp_number = config_df.iloc[0]['numero']
                    whatsapp_link = f"https://wa.me/+55{whatsapp_number}?text={mensagem_encoded}"
                    st.markdown(f'<a href="{whatsapp_link}" target="_blank">Enviar pedido por WhatsApp</a>', unsafe_allow_html=True)
                    st.session_state.cart = []
                    st.success("Pedido enviado! Retornando à loja...")
                    st.session_state.show_cart = False
                    st.rerun()
                except:
                    st.error("Erro ao processar pedido. Tente novamente.")

# Grid de produtos
if not st.session_state.show_cart:
    st.markdown('<div class="product-grid">', unsafe_allow_html=True)
    for idx, produto in produtos_filtrados.iterrows():
        st.markdown(f"""
        <div class="product-card">
            <div class="product-image-container">
                <img src="uploads/{produto['imagem_path']}" class="product-image" 
                     onerror="this.src='https://via.placeholder.com/300x300?text=Sem+Imagem'">
            </div>
            <div class="product-info">
                <div class="product-name">{produto['nome']}</div>
                <div class="product-price">R$ {produto['preco_venda']:.2f}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Ver Detalhes", key=f"details_{idx}", use_container_width=True):
                st.session_state.show_product_details = produto
        with col2:
            if st.button("Comprar", key=f"buy_{idx}", type="primary", use_container_width=True):
                st.session_state.cart.append({
                    'codigo': produto['codigo'],
                    'nome': produto['nome'],
                    'preco': produto['preco_venda'],
                    'tamanho': produto['tamanho'],
                    'cor': produto['cor'],
                    'quantidade': 1
                })
                st.success("✅ Produto adicionado ao carrinho!")
    st.markdown('</div>', unsafe_allow_html=True)

# Modal de detalhes do produto
if st.session_state.show_product_details is not None:
    produto = st.session_state.show_product_details
    with st.container():
        col1, col2 = st.columns([1,2])
        with col1:
            st.image(f"uploads/{produto['imagem_path']}", use_column_width=True)
        with col2:
            st.title(produto['nome'])
            st.markdown(f"**Categoria:** {produto['categoria']}")
            st.markdown(f"**Descrição:**\n{produto.get('descricao', '')}")
            st.markdown(f"**Preço:** R$ {produto['preco_venda']:.2f}")
            st.markdown(f"**Cor:** {produto['cor']}")
            st.markdown(f"**Tamanho:** {produto['tamanho']}")
            
            if st.button("Fechar"):
                st.session_state.show_product_details = None
                st.rerun()
