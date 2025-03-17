import streamlit as st
import pandas as pd
from utils import gerar_sugestoes, formatar_sugestoes
from utils import load_data
from auth import check_password

if not check_password():
    st.stop()

st.title("Assistente de IA")

# CSS para animação de carregamento personalizada
st.markdown("""
<style>
.loader {
    width: 50px;
    height: 50px;
    border: 5px solid #f3f3f3;
    border-top: 5px solid #FF4B4B;
    border-radius: 50%;
    animation: spin 1s linear infinite;
    margin: 20px auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loader-container {
    text-align: center;
    padding: 20px;
}

.loader-text {
    color: #FF4B4B;
    font-size: 16px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.write("""
### Análise Inteligente de Dados
O assistente utiliza algoritmos de aprendizado de máquina para analisar:
- Tendências de vendas
- Níveis de estoque
- Sugestões de reposição
""")

# Carregando dados
produtos_df = load_data("produtos")
financeiro_df = load_data("financeiro")

# Botão para gerar sugestões
if st.button("Gerar Sugestões", key="gerar_sugestoes"):
    # Criar container para animação
    loading_container = st.empty()

    # Mostrar animação de carregamento
    loading_container.markdown("""
    <div class="loader-container">
        <div class="loader"></div>
        <div class="loader-text">Analisando dados e gerando sugestões...</div>
    </div>
    """, unsafe_allow_html=True)

    # Gerando sugestões
    sugestoes = gerar_sugestoes(produtos_df, financeiro_df)
    texto_sugestoes = formatar_sugestoes(sugestoes)

    # Limpar animação antes de mostrar resultados
    loading_container.empty()

    # Exibindo sugestões
    st.header("Sugestões do Assistente")

    if texto_sugestoes:
        for sugestao in texto_sugestoes:
            st.markdown(sugestao)
            st.divider()
    else:
        st.info("Não há sugestões disponíveis no momento. Isso pode acontecer se não houver dados suficientes para análise.")

# Explicação da análise
with st.expander("Como funciona a análise?"):
    st.write("""
    1. **Análise de Vendas**: O sistema analisa as tendências de vendas dos últimos 30 dias 
       utilizando regressão linear para identificar padrões.

    2. **Análise de Estoque**: São identificados produtos com quantidade menor ou igual a 5 
       unidades, considerados como estoque crítico.

    3. **Sugestões Automáticas**: Com base nas análises, o sistema gera sugestões 
       personalizadas para ajudar na gestão do negócio.
    """)