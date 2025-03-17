import streamlit as st
import pandas as pd
from utils.ai_assistant import gerar_sugestoes, formatar_sugestoes
from utils import load_data
from auth import check_password

if not check_password():
    st.stop()

st.title("Assistente de IA")

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

# Gerando sugestões
sugestoes = gerar_sugestoes(produtos_df, financeiro_df)
texto_sugestoes = formatar_sugestoes(sugestoes)

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
