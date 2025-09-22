import streamlit as st
import requests

st.set_page_config(page_title="Plano de Estudos - Tech + Saúde", layout="wide")

st.title("📅 Plano de Estudos Tech + Saúde")
st.write("Marque as atividades concluídas. O progresso será salvo direto no Firebase.")

# -----------------------------
# CONFIG FIREBASE
# -----------------------------
# 🔥 Coloque aqui a URL do seu Firebase Realtime Database
# Exemplo: "https://SEU-PROJETO-default-rtdb.firebaseio.com"
FIREBASE_URL = "https://console.firebase.google.com/u/1/project/study-a5b49/database/study-a5b49-default-rtdb/data/~2F?hl=pt-br"

# Função para carregar progresso
def carregar_progresso():
    url = f"{FIREBASE_URL}/progresso.json"
    try:
        res = requests.get(url)
        if res.status_code == 200 and res.json():
            return res.json()
    except Exception as e:
        st.error(f"Erro ao carregar progresso: {e}")
    return {}

# Função para salvar progresso
def salvar_progresso(progresso):
    url = f"{FIREBASE_URL}/progresso.json"
    try:
        res = requests.put(url, json=progresso)
        return res.status_code == 200
    except Exception as e:
        st.error(f"Erro ao salvar: {e}")
        return False

# -----------------------------
# PLANO DE ESTUDOS
# -----------------------------
plano_estudos = {
    "Segunda-feira (2h)": [
        "Suzano - Python Developer #2 (1h30)",
        "Exercícios práticos (30min)"
    ],
    "Terça-feira (2h)": [
        "Formação CSS Web Developer (1h30)",
        "Exercícios físicos (musculação em casa) (30min)"
    ],
    "Quarta-feira (2h)": [
        "Formação React Developer (1h30)",
        "Exercícios práticos (30min)"
    ],
    "Quinta-feira (2h)": [
        "Formação JavaScript Developer (1h30)",
        "Exercícios físicos (musculação em casa) (30min)"
    ],
    "Sexta-feira (2h)": [
        "Cursos/Imersões paralelos (IA, BD, Ciência de Dados) (1h30)",
        "Exercícios práticos (30min)"
    ],
    "Sábado (até 6h – tarde/noite)": [
        "Python Developer (1h30)",
        "CSS Web Developer (1h)",
        "React Developer (1h)",
        "JavaScript Developer (1h)",
        "Exercícios práticos (30min)",
        "Cursos/Imersões paralelos (1h)",
        "Exercícios físicos (musculação em casa) (30min)"
    ],
    "Domingo (até 6h – manhã/tarde/noite)": [
        "Python Developer (1h)",
        "CSS Web Developer (1h)",
        "React Developer (1h)",
        "JavaScript Developer (1h)",
        "Cursos/Imersões paralelos (1h)",
        "Projetos práticos/Desafios (30min)",
        "Exercícios físicos (musculação em casa) (30min)"
    ]
}

# -----------------------------
# APP STREAMLIT
# -----------------------------
progresso = carregar_progresso()

for dia, atividades in plano_estudos.items():
    st.subheader(dia)
    for atividade in atividades:
        checked = progresso.get(dia, {}).get(atividade, False)
        novo_estado = st.checkbox(atividade, value=checked, key=f"{dia}-{atividade}")

        if dia not in progresso:
            progresso[dia] = {}
        progresso[dia][atividade] = novo_estado

if st.button("💾 Salvar progresso no Firebase"):
    if salvar_progresso(progresso):
        st.success("✅ Progresso salvo com sucesso no Firebase!")
    else:
        st.error("❌ Erro ao salvar. Verifique sua URL do Firebase.")

