import streamlit as st
import pandas as pd

def check_password():
    """Retorna `True` se o usuário tiver a senha correta."""
    def login_form():
        """Form de login"""
        with st.form("Autenticação"):
            st.markdown("### Login")
            usuario = st.text_input("Usuário")
            senha = st.text_input("Senha", type="password")
            return usuario, senha, st.form_submit_button("Entrar")

    # Retorna True se a autenticação já foi feita
    if st.session_state.get("authenticated"):
        return True

    # Mostra o form de login
    usuario, senha, submitted = login_form()

    if submitted:
        # Verifica as credenciais
        usuarios_df = pd.read_csv("data/usuarios.csv")
        if usuario in usuarios_df['usuario'].values:
            user_data = usuarios_df[usuarios_df['usuario'] == usuario]
            if user_data['senha'].iloc[0] == senha:
                st.session_state["authenticated"] = True
                return True
        
        st.error("Usuário ou senha incorretos")
        return False

    return False
