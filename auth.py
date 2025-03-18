
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
            background: transparent;
        }
        .login-container {
            max-width: 500px;
            margin: 0 auto;
            padding: 30px;
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        }
        .big-logo {
            width: 300px;
            margin: 0 auto 20px auto;
            display: block;
        }
        #background-video {
            position: fixed;
            right: 0;
            bottom: 0;
            min-width: 100%;
            min-height: 100%;
            z-index: -1;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Carrega o vídeo de fundo se existir
        if os.path.exists("background.mp4"):
            st.markdown("""
            <video autoplay muted loop id="background-video">
                <source src="background.mp4" type="video/mp4">
            </video>
            """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            st.markdown("""
            <style>
            .login-container {
                background: linear-gradient(145deg, #ffffff, #f0f0f0);
                box-shadow: 20px 20px 60px #bebebe, -20px -20px 60px #ffffff;
                border-radius: 15px;
                padding: 30px;
                max-width: 400px;
                margin: 0 auto;
            }
            .stButton > button {
                background: linear-gradient(145deg, #007bff, #0056b3);
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                transition: all 0.3s ease;
            }
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
            </style>
            """, unsafe_allow_html=True)
            
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            with st.form("Autenticação"):
                try:
                    if os.path.exists("logo.png"):
                        st.image("logo.png", width=300)
                    st.markdown("### Sistema de Gestão", help="Bem-vindo ao sistema")
                except:
                    st.info("⚠️ Logo não encontrada")
                    st.markdown("### Sistema de Gestão", help="Bem-vindo ao sistema")
                usuario = st.text_input("👤 Usuário", placeholder="Digite seu usuário")
                senha = st.text_input("🔒 Senha", type="password", placeholder="Digite sua senha")
                submitted = st.form_submit_button("Entrar", use_container_width=True)
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
