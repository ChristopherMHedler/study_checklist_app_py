import streamlit as st
import requests
import datetime
import pandas as pd

st.set_page_config(page_title="Plano de Estudos - Tech + Saúde", layout="wide")

st.title("📅 Plano de Estudos Tech + Saúde")
st.write("Monte e acompanhe seu cronograma. O progresso será salvo no Firebase.")

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
data_inicio = st.sidebar.date_input("Data de início", datetime.date.today())
quant_semanas = st.sidebar.number_input("Quantas semanas?", min_value=1, max_value=52, value=12)

# -----------------------------
# GERENCIAR CURSOS
# -----------------------------
st.sidebar.subheader("📚 Cursos")

# Se não existir ainda, inicializa
if "cursos" not in st.session_state:
    st.session_state["cursos"] = ["Curso principal (1h30)", "Exercícios práticos (30min)"]

if "plano_estudos" not in st.session_state:
    st.session_state["plano_estudos"] = {}

# Input para adicionar curso
novo_curso = st.sidebar.text_input("Adicionar novo curso")
if st.sidebar.button("➕ Adicionar curso") and novo_curso:
    if novo_curso not in st.session_state["cursos"]:
        st.session_state["cursos"].append(novo_curso)
    st.sidebar.success(f"Curso '{novo_curso}' adicionado!")
    st.experimental_rerun()

# Remover curso
curso_remover = st.sidebar.selectbox("Remover curso", [""] + st.session_state["cursos"])
if st.sidebar.button("🗑️ Remover curso") and curso_remover:
    if curso_remover in st.session_state["cursos"]:
        st.session_state["cursos"].remove(curso_remover)
        # Remove também do plano_estudos
        for dia in st.session_state["plano_estudos"]:
            if curso_remover in st.session_state["plano_estudos"][dia]:
                st.session_state["plano_estudos"][dia].remove(curso_remover)
    st.experimental_rerun()

# -----------------------------
# PLANO POR DIA
# -----------------------------
dias_semana = [
    "Segunda-feira",
    "Terça-feira",
    "Quarta-feira",
    "Quinta-feira",
    "Sexta-feira",
    "Sábado",
    "Domingo"
]

st.sidebar.subheader("📅 Atividades por dia")

for dia in dias_semana:
    if dia not in st.session_state["plano_estudos"]:
        st.session_state["plano_estudos"][dia] = []

    atividades_dia = st.sidebar.multiselect(
        f"{dia} - selecione cursos:",
        options=st.session_state["cursos"],
        default=st.session_state["plano_estudos"][dia],
        key=f"multiselect_{dia}"
    )
    st.session_state["plano_estudos"][dia] = atividades_dia

# -----------------------------
# GERAR CALENDÁRIO DE ESTUDOS
# -----------------------------
datas_com_atividades = {}
for semana in range(quant_semanas):
    for i, dia in enumerate(dias_semana):
        data_atual = data_inicio + datetime.timedelta(days=(semana * 7) + i)
        data_formatada = data_atual.strftime("%d/%m/%Y")
        titulo = f"{dia} - {data_formatada}"
        datas_com_atividades[titulo] = st.session_state["plano_estudos"][dia]

# -----------------------------
# APP STREAMLIT
# -----------------------------
progresso = carregar_progresso()

for dia, atividades in datas_com_atividades.items():
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

# -----------------------------
# EXPORTAR PARA EXCEL
# -----------------------------
if st.button("📊 Exportar cronograma para Excel"):
    linhas = []
    for dia, atividades in datas_com_atividades.items():
        for atividade in atividades:
            concluido = progresso.get(dia, {}).get(atividade, False)
            linhas.append({
                "Data": dia.split(" - ")[1],
                "Dia": dia.split(" - ")[0],
                "Atividade": atividade,
                "Concluído": "✅" if concluido else "❌"
            })

    df = pd.DataFrame(linhas)
    arquivo_excel = "plano_estudos.xlsx"
    df.to_excel(arquivo_excel, index=False)

    with open(arquivo_excel, "rb") as f:
        st.download_button(
            label="⬇️ Baixar Excel",
            data=f,
            file_name=arquivo_excel,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
