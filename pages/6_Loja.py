
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
    position: relative;
    overflow: hidden;
}
.product-card:hover {
    transform: translateY(-5px);
}
.product-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 8px;
    margin-bottom: 10px;
}
.price {
    font-size: 24px;
    color: #2ecc71;
    font-weight: bold;
    margin: 10px 0;
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
    position: absolute;
    bottom: 15px;
    left: 0;
    right: 0;
    margin: 0 15px;
    width: calc(100% - 30px);
}
.buy-button:hover {
    background-color: #27ae60;
}
.description-preview {
    height: 60px;
    overflow: hidden;
    margin-bottom: 40px;
}
.modal {
    display: none;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0,0,0,0.7);
    z-index: 1000;
}
.modal-content {
    background: white;
    padding: 20px;
    border-radius: 10px;
    max-width: 800px;
    width: 90%;
    margin: 50px auto;
    max-height: 80vh;
    overflow-y: auto;
}
.cart-item {
    background: #f8f9fa;
    padding: 15px;
    border-radius: 8px;
    margin: 10px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.cart-total {
    font-size: 24px;
    font-weight: bold;
    text-align: right;
    padding: 20px;
    border-top: 2px solid #eee;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# Inicializar carrinho na sessão
if 'cart' not in st.session_state:
    st.session_state.cart = []
    st.session_state.show_cart = False
    st.session_state.selected_product = None

# Carregar produtos e configurações
produtos_df = pd.read_csv("data/produtos.csv")
try:
    whatsapp_config = pd.read_csv("data/whatsapp_config.csv").iloc[0]
except:
    whatsapp_config = {'numero': '', 'mensagem_padrao': ''}

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
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🛍️ Loja Xible")
    st.markdown("### Encontre os melhores produtos aqui!")

with col2:
    if st.button(f"🛒 Carrinho ({len(st.session_state.cart)})", key="cart_button"):
        st.session_state.show_cart = True

# Modal do Carrinho
if st.session_state.show_cart:
    with st.container():
        st.markdown("## 🛒 Seu Carrinho")
        
        if not st.session_state.cart:
            st.info("Seu carrinho está vazio")
        else:
            total = 0
            for idx, item in enumerate(st.session_state.cart):
                col1, col2, col3 = st.columns([3,1,1])
                with col1:
                    st.markdown(f"""
                    #### {item['nome']}
                    Tamanho: {item['tamanho']} | Cor: {item['cor']}
                    Preço: R$ {item['preco']:.2f} x {item['quantidade']}
                    """)
                with col2:
                    qty_col1, qty_col2, qty_col3 = st.columns(3)
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
                    if st.button("🗑️", key=f"remove_{idx}"):
                        st.session_state.cart.pop(idx)
                        st.rerun()
                
                total += item['preco'] * item['quantidade']
                st.markdown("---")
            
            st.markdown(f"### Total: R$ {total:.2f}")
            
            if st.button("Finalizar Compra", type="primary"):
                itens = "\n".join([
                    f"- {item['nome']} ({item['cor']}, {item['tamanho']}) x{item['quantidade']} = R$ {item['preco'] * item['quantidade']:.2f}"
                    for item in st.session_state.cart
                ])
                
                mensagem = whatsapp_config['mensagem_padrao'].format(
                    itens=itens,
                    total=total
                )
                
                mensagem_encoded = mensagem.replace('\n', '%0A').replace(' ', '%20')
                whatsapp_link = f"https://wa.me/+55{whatsapp_config['numero']}?text={mensagem_encoded}"
                st.markdown(f'<a href="{whatsapp_link}" target="_blank" class="whatsapp-button">Enviar pedido por WhatsApp</a>', unsafe_allow_html=True)
                st.session_state.cart = []
                st.rerun()
            
            if st.button("Continuar Comprando"):
                st.session_state.show_cart = False
                st.rerun()

# Grid de produtos
if not st.session_state.show_cart:
    cols = st.columns(3)
    for idx, produto in produtos_filtrados.iterrows():
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="product-card">
                <img src="uploads/{produto['imagem_path']}" class="product-image" onerror="this.src='https://via.placeholder.com/300x200?text=Sem+Imagem'">
                <span class="category-tag">{produto['categoria']}</span>
                <h3>{produto['nome']}</h3>
                <div class="description-preview">{produto.get('descricao', '')}</div>
                <div class="price">R$ {produto['preco_venda']:.2f}</div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Ver Detalhes", key=f"details_{idx}"):
                st.session_state.selected_product = produto
                
            if st.button("Comprar", key=f"buy_{idx}", type="primary"):
                item = {
                    'codigo': produto['codigo'],
                    'nome': produto['nome'],
                    'preco': produto['preco_venda'],
                    'tamanho': produto['tamanho'],
                    'cor': produto['cor'],
                    'quantidade': 1
                }
                st.session_state.cart.append(item)
                st.success("✅ Produto adicionado ao carrinho!")

# Modal de detalhes do produto
if st.session_state.selected_product is not None:
    with st.expander("Detalhes do Produto", expanded=True):
        col1, col2 = st.columns([1,2])
        with col1:
            st.image(f"uploads/{st.session_state.selected_product['imagem_path']}", use_column_width=True)
        with col2:
            st.title(st.session_state.selected_product['nome'])
            st.markdown(f"**Categoria:** {st.session_state.selected_product['categoria']}")
            st.markdown(f"**Descrição:**\n{st.session_state.selected_product.get('descricao', '')}")
            st.markdown(f"**Preço:** R$ {st.session_state.selected_product['preco_venda']:.2f}")
            st.markdown(f"**Cor:** {st.session_state.selected_product['cor']}")
            st.markdown(f"**Tamanho:** {st.session_state.selected_product['tamanho']}")
            
            if st.button("Fechar"):
                st.session_state.selected_product = None
                st.rerun()
