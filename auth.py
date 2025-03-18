
import streamlit as st
import pandas as pd
import os

def check_password():
    """Retorna `True` se o usuário tiver a senha correta."""
    def login_form():
        """Form de login"""
        st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .login-container {
            max-width: 400px;
            margin: 0 auto;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            with st.form("Autenticação"):
                st.markdown("### Sistema de Gestão")
                try:
                    if os.path.exists("logo.png"):
                        st.image("logo.png", width=200)
                except:
                    st.info("⚠️ Logo não encontrada")
                usuario = st.text_input("👤 Usuário")
                senha = st.text_input("🔒 Senha", type="password")
                col1, col2 = st.columns(2)
                with col1:
                    submitted = st.form_submit_button("Entrar", use_container_width=True)
                with col2:
                    if st.form_submit_button("Configurações", use_container_width=True):
                        st.session_state.show_config = True
                st.markdown('</div>', unsafe_allow_html=True)
                return usuario, senha, submitted

    if st.session_state.get("show_config", False):
        st.markdown("### ⚙️ Configurações")
        uploaded_file = st.file_uploader("Upload da Logo", type=['png', 'jpg', 'jpeg'])
        if uploaded_file is not None:
            with open("logo.png", "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("Logo atualizada com sucesso!")
        if st.button("Voltar"):
            st.session_state.show_config = False
            st.rerun()
        return False

    if st.session_state.get("authenticated"):
        return True

    usuario, senha, submitted = login_form()

    if submitted:
        usuarios_df = pd.read_csv("data/usuarios.csv")
        if usuario in usuarios_df['usuario'].values:
            user_data = usuarios_df[usuarios_df['usuario'] == usuario]
            if user_data['senha'].iloc[0] == senha:
                st.session_state["authenticated"] = True
                return True
        st.error("❌ Usuário ou senha incorretos")
        return False

    return False
