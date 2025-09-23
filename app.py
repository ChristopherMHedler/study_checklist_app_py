import streamlit as st
import requests
import datetime
import pandas as pd

st.set_page_config(page_title="Plano de Estudos - Tech + Saúde", layout="wide")

st.title("📅 Plano de Estudos Tech + Saúde")
st.write("Marque as atividades concluídas. O progresso será salvo direto no Firebase.")

# -----------------------------
# CONFIG FIREBASE
# -----------------------------
FIREBASE_URL = "https://study-a5b49-default-rtdb.firebaseio.com/"

def carregar_progresso():
    url = f"{FIREBASE_URL}/progresso.json"
    try:
        res = requests.get(url)
        if res.status_code == 200 and res.json():
            return res.json()
    except Exception as e:
        st.error(f"Erro ao carregar progresso: {e}")
    return {}

def salvar_progresso(progresso):
    url = f"{FIREBASE_URL}/progresso.json"
    try:
        res = requests.put(url, json=progresso)
        return res.status_code == 200
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

# -----------------------------
# CONFIGURAÇÕES DO USUÁRIO
# -----------------------------
st.sidebar.header("⚙️ Configurações do Plano")
data_inicio = st.sidebar.date_input("Data de início", datetime.date(2025, 9, 22))
quant_semanas = st.sidebar.number_input("Quantas semanas?", min_value=1, max_value=52, value=12)

st.sideba
