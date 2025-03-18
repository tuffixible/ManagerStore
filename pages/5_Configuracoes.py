
import streamlit as st
from auth import check_password
import os

if not check_password():
    st.stop()

st.title("⚙️ Configurações do Sistema")

uploaded_file = st.file_uploader("Upload da Logo", type=['png', 'jpg', 'jpeg'])
if uploaded_file is not None:
    with open("logo.png", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("✅ Logo atualizada com sucesso!")
    st.image("logo.png", width=200)

st.divider()

# Configurações adicionais podem ser adicionadas aqui
st.subheader("Configurações de Usuário")
with st.expander("Alterar Senha"):
    with st.form("alterar_senha"):
        senha_atual = st.text_input("Senha Atual", type="password")
        nova_senha = st.text_input("Nova Senha", type="password")
        confirmar_senha = st.text_input("Confirmar Nova Senha", type="password")
        if st.form_submit_button("Alterar Senha"):
            if nova_senha == confirmar_senha:
                st.success("Senha alterada com sucesso!")
            else:
                st.error("As senhas não conferem!")
