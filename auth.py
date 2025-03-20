
import streamlit as st
import pandas as pd
import os
from datetime import datetime

def check_password():
    """Retorna `True` se o usuário tiver a senha correta."""
    def login_form():
        """Form de login moderno"""
        st.markdown("""
        <style>
        .stApp {
            background: transparent;
        }
        .login-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 30px;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            animation: fadeIn 0.5s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .big-logo {
            width: 300px;
            margin: 0 auto 20px auto;
            display: block;
        }
        .input-container {
            margin: 15px 0;
            position: relative;
        }
        .input-container input {
            width: 100%;
            padding: 10px 15px;
            border: 1px solid #ddd;
            border-radius: 8px;
            transition: all 0.3s ease;
        }
        .input-container input:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 5px rgba(76, 175, 80, 0.3);
        }
        .forgot-password {
            text-align: right;
            font-size: 0.9em;
            color: #666;
            margin: 10px 0;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            with st.form("Autenticação"):
                st.markdown("### 🏪 Sistema de Gestão", help="Bem-vindo ao sistema")
                
                try:
                    if os.path.exists("logo.png"):
                        st.image("logo.png", width=200)
                except:
                    pass
                
                usuario = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
                senha = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
                
                if st.checkbox("Esqueceu a senha?"):
                    st.info("Entre em contato com o administrador do sistema para redefinir sua senha.")
                
                submitted = st.form_submit_button("Entrar", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                if submitted:
                    # Registrar tentativa de login
                    with open("data/login_attempts.log", "a") as f:
                        f.write(f"{datetime.now()},{usuario},{'success' if check_credentials(usuario, senha) else 'failed'}\n")
                
                return usuario, senha, submitted

    def check_credentials(usuario, senha):
        """Verifica credenciais e retorna o perfil do usuário"""
        usuarios_df = pd.read_csv("data/usuarios.csv")
        if usuario in usuarios_df['usuario'].values:
            user_data = usuarios_df[usuarios_df['usuario'] == usuario]
            if user_data['senha'].iloc[0] == senha:
                perfil = user_data['perfil'].iloc[0]
st.session_state['user_role'] = perfil
st.session_state['permissions'] = {
    'produtos_view': perfil in ['administrador', 'gerente', 'vendedor'],
    'produtos_edit': perfil in ['administrador', 'gerente'],
    'financeiro_view': perfil in ['administrador', 'gerente'],
    'financeiro_edit': perfil in ['administrador'],
    'relatorios_view': perfil in ['administrador', 'gerente'],
    'config_view': perfil in ['administrador'],
    'config_edit': perfil in ['administrador']
}
                st.session_state['user_name'] = usuario
                return True
        return False

    if st.session_state.get("authenticated"):
        return True

    usuario, senha, submitted = login_form()

    if submitted and check_credentials(usuario, senha):
        st.session_state["authenticated"] = True
        st.success(f"👋 Bem-vindo, {usuario}!")
        st.rerun()
    elif submitted:
        st.error("❌ Usuário ou senha incorretos")
        return False

    return False
