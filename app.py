import json
from pathlib import Path
from datetime import datetime

import streamlit as st

ARQUIVO_MENSAGENS = Path("mensagens.json")

def carregar_mensagens():
     
    if not ARQUIVO_MENSAGENS.exists():
        return []


    try:
        with open(ARQUIVO_MENSAGENS, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def salvar_mensagens(mensagens):

    with open(ARQUIVO_MENSAGENS, "w", encoding="utf-8") as f:
        json.dump(mensagens, f, indent=4, ensure_ascii=False)

def adicionar_mensagem(username,mensagem):
   
    mensagens = carregar_mensagens()


    horario = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")


    mensagens.insert(
        0,
        {
            "time": f"({horario})",
            "username": username,
            "mensagem": mensagem,
        },
    )


    salvar_mensagens(mensagens)

st.title("💬 Chat entre usuários ")

username = st.sidebar.text_input("Nome de usuário", key="username",value="AnÔnimo")

@st.fragment(run_every=3)
def renderizar_chat(): 
    mensagens = carregar_mensagens()

    with st.container(border=True, height=500):
        for msg in mensagens:
          st.write(f'{msg["time"]}): - {msg["username"]}: -{msg["mensagem"]}')

renderizar_chat()

entrada_usuario = st.chat_input("Digite uma mensagem")

if entrada_usuario:
    adicionar_mensagem(username , entrada_usuario)
    st.rerun()