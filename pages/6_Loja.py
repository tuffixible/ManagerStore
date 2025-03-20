
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
.cart-button {
    position: fixed;
    top: 20px;
    right: 20px;
    background-color: #2ecc71;
    color: white;
    padding: 10px 20px;
    border-radius: 25px;
    cursor: pointer;
    z-index: 1000;
    display: flex;
    align-items: center;
    gap: 10px;
}
.cart-count {
    background-color: white;
    color: #2ecc71;
    border-radius: 50%;
    padding: 2px 8px;
    font-size: 14px;
}
.cart-panel {
    position: fixed;
    top: 0;
    right: 0;
    width: 400px;
    height: 100vh;
    background: white;
    box-shadow: -2px 0 5px rgba(0,0,0,0.1);
    padding: 20px;
    z-index: 1001;
    overflow-y: auto;
}
.cart-item {
    background: #f8f9fa;
    padding: 10px;
    margin: 10px 0;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# Inicializar carrinho na sessão
if 'cart' not in st.session_state:
    st.session_state.cart = []
    st.session_state.show_cart = False

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
col1, col2 = st.columns([4, 1])
with col1:
    st.title("🛍️ Loja Xible")
    st.markdown("### Encontre os melhores produtos aqui!")

with col2:
    if st.button(f"🛒 Carrinho ({len(st.session_state.cart)})", key="cart_button"):
        st.session_state.show_cart = not st.session_state.show_cart

# Mostrar carrinho
if st.session_state.show_cart:
    with st.sidebar:
        st.title("🛒 Carrinho")
        total = 0
        
        for idx, item in enumerate(st.session_state.cart):
            with st.container():
                st.markdown(f"""
                #### {item['nome']}
                Tamanho: {item['tamanho']} | Cor: {item['cor']}
                Preço: R$ {item['preco']:.2f} x {item['quantidade']} = R$ {item['preco'] * item['quantidade']:.2f}
                """)
                col1, col2, col3 = st.columns([1,2,1])
                with col1:
                    if st.button("-", key=f"minus_{idx}"):
                        if item['quantidade'] > 1:
                            st.session_state.cart[idx]['quantidade'] -= 1
                            st.rerun()
                with col2:
                    st.write(f"Quantidade: {item['quantidade']}")
                with col3:
                    if st.button("+", key=f"plus_{idx}"):
                        st.session_state.cart[idx]['quantidade'] += 1
                        st.rerun()
                if st.button("Remover", key=f"remove_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
                total += item['preco'] * item['quantidade']
        
        if st.session_state.cart:
            st.markdown(f"### Total: R$ {total:.2f}")
            
            vendedores = pd.read_csv("data/usuarios.csv")
            vendedores = vendedores[vendedores['perfil'] == 'vendedor']
            vendedor = st.selectbox("Escolha um vendedor:", vendedores['usuario'])
            
            if st.button("Finalizar Compra"):
                mensagem = "Olá! Gostaria de fazer um pedido:\n\n"
                for item in st.session_state.cart:
                    mensagem += f"- {item['nome']} ({item['cor']}, Tam: {item['tamanho']})\n"
                    mensagem += f"  Quantidade: {item['quantidade']} x R$ {item['preco']:.2f} = R$ {item['preco'] * item['quantidade']:.2f}\n"
                mensagem += f"\nTotal: R$ {total:.2f}"
                
                mensagem_encoded = mensagem.replace('\n', '%0A').replace(' ', '%20')
                whatsapp_link = f"https://wa.me/+55{vendedores[vendedores['usuario'] == vendedor]['telefone'].iloc[0]}?text={mensagem_encoded}"
                st.markdown(f'<a href="{whatsapp_link}" target="_blank" class="whatsapp-button">Enviar pedido por WhatsApp</a>', unsafe_allow_html=True)
                st.session_state.cart = []
        else:
            st.info("Seu carrinho está vazio")

# Grid de produtos
cols = st.columns(3)
for idx, produto in produtos_filtrados.iterrows():
    with cols[idx % 3]:
        if st.button("Comprar", key=f"buy_{produto['codigo']}", type="primary"):
            item = {
                'codigo': produto['codigo'],
                'nome': produto['nome'],
                'preco': produto['preco_venda'],
                'tamanho': produto['tamanho'],
                'cor': produto['cor'],
                'quantidade': 1
            }
            st.session_state.cart.append(item)
            st.rerun()
        
        st.markdown(f"""
        <div class="product-card">
            <img src="{produto.get('imagem', 'default.jpg')}" class="product-image">
            <span class="category-tag">{produto['categoria']}</span>
            <h3>{produto['nome']}</h3>
            <p>{produto.get('descricao', '')}</p>
            <div class="price">R$ {produto['preco_venda']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)
