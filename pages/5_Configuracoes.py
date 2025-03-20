import streamlit as st
from auth import check_password
import os
import shutil
import pandas as pd

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

# Configurações de Notificações WhatsApp
st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.subheader("📱 Configurações de WhatsApp")

# Load existing WhatsApp settings
if 'whatsapp_config' not in st.session_state:
    try:
        whatsapp_df = pd.read_csv("data/whatsapp_config.csv")
        st.session_state.whatsapp_config = whatsapp_df.to_dict('records')[0]
    except:
        st.session_state.whatsapp_config = {
            'numero': '',
            'mensagem_padrao': 'Olá! Gostaria de fazer um pedido:\n\n{itens}\n\nTotal: R$ {total}',
            'ativar_notificacoes': False
        }

col1, col2 = st.columns(2)
with col1:
    numero = st.text_input(
        "Número do WhatsApp (com DDD)", 
        value=st.session_state.whatsapp_config['numero'],
        placeholder="Ex: 11999999999"
    )

with col2:
    enable_notifications = st.checkbox(
        "Ativar notificações automáticas",
        value=st.session_state.whatsapp_config['ativar_notificacoes']
    )

mensagem_padrao = st.text_area(
    "Mensagem padrão do pedido",
    value=st.session_state.whatsapp_config['mensagem_padrao'],
    help="Use {itens} para lista de produtos e {total} para valor total"
)

if st.button("💾 Salvar Configurações de WhatsApp"):
    config = {
        'numero': numero,
        'mensagem_padrao': mensagem_padrao,
        'ativar_notificacoes': enable_notifications
    }
    pd.DataFrame([config]).to_csv("data/whatsapp_config.csv", index=False)
    st.session_state.whatsapp_config = config
    st.success("✅ Configurações de WhatsApp salvas com sucesso!")
st.markdown('</div>', unsafe_allow_html=True)

# Gerenciamento de Permissões
st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.subheader("👥 Gerenciamento de Permissões")

if st.session_state.get('user_role') == 'administrador':
    usuarios_df = pd.read_csv("data/usuarios.csv")

    # Definir permissões disponíveis
    permissoes = {
        'produtos_view': 'Visualizar Produtos',
        'produtos_edit': 'Editar Produtos',
        'financeiro_view': 'Visualizar Financeiro',
        'financeiro_edit': 'Editar Financeiro',
        'relatorios_view': 'Visualizar Relatórios',
        'config_view': 'Acessar Configurações',
        'config_edit': 'Editar Configurações'
    }

    # Criar interface de edição
    edited_df = st.data_editor(
        usuarios_df,
        column_config={
            "usuario": "Usuário",
            "perfil": st.column_config.SelectboxColumn(
                "Perfil",
                options=["administrador", "gerente", "vendedor", "cliente"],
                required=True
            ),
            "email": "Email"
        },
        hide_index=True,
        num_rows="dynamic"
    )

    if st.button("Salvar Alterações"):
        edited_df.to_csv("data/usuarios.csv", index=False)
        st.success("✅ Permissões atualizadas com sucesso!")
else:
    st.warning("Apenas administradores podem gerenciar permissões.")
st.markdown('</div>', unsafe_allow_html=True)

# Easter Egg Settings
st.markdown('<div class="config-card">', unsafe_allow_html=True)
st.subheader("🎮 Easter Eggs")
if 'show_easter_egg' not in st.session_state:
    st.session_state.show_easter_egg = True

show_easter_egg = st.toggle("Mostrar pássaro voador", value=st.session_state.show_easter_egg)
if show_easter_egg != st.session_state.show_easter_egg:
    st.session_state.show_easter_egg = show_easter_egg
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)