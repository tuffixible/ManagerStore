
import streamlit as st
from auth import check_password
import os
import shutil

if not check_password():
    st.stop()

st.title("⚙️ Configurações do Sistema")

# Estilo para cards
st.markdown("""
<style>
.config-card {
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Upload da Logo
st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.subheader("🖼️ Logo da Empresa")
uploaded_file = st.file_uploader("Upload da Logo", type=['png', 'jpg', 'jpeg'])
if uploaded_file is not None:
    with open("logo.png", "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success("✅ Logo atualizada com sucesso!")
    st.image("logo.png", width=200)
st.markdown('</div>', unsafe_allow_html=True)

# Upload do Vídeo de Fundo
st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.subheader("🎥 Vídeo de Fundo")
st.info("O vídeo será usado como plano de fundo na tela de login")
video_file = st.file_uploader("Upload do Vídeo de Fundo", type=['mp4'])
if video_file is not None:
    with open("background.mp4", "wb") as f:
        f.write(video_file.getbuffer())
    st.success("✅ Vídeo de fundo atualizado com sucesso!")
    st.video(video_file)
st.markdown('</div>', unsafe_allow_html=True)

# Configurações de Usuário
st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.subheader("👤 Configurações de Usuário")
with st.expander("🔐 Alterar Senha"):
    with st.form("alterar_senha"):
        senha_atual = st.text_input("Senha Atual", type="password")
        nova_senha = st.text_input("Nova Senha", type="password")
        confirmar_senha = st.text_input("Confirmar Nova Senha", type="password")
        if st.form_submit_button("Alterar Senha"):
            if nova_senha == confirmar_senha:
                st.success("✅ Senha alterada com sucesso!")
            else:
                st.error("❌ As senhas não conferem!")
st.markdown('</div>', unsafe_allow_html=True)
