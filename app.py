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
FIREBASE_URL = "https://SEU-PROJETO.firebaseio.com"

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

st.sidebar.write("✏️ Personalize as atividades de cada dia:")

plano_estudos = {}
dias_semana = [
    "Segunda-feira (2h)",
    "Terça-feira (2h)",
    "Quarta-feira (2h)",
    "Quinta-feira (2h)",
    "Sexta-feira (2h)",
    "Sábado (até 6h – tarde/noite)",
    "Domingo (até 6h – manhã/tarde/noite)"
]

for dia in dias_semana:
    st.sidebar.subheader(dia)
    atividades = st.sidebar.text_area(
        f"Atividades para {dia}",
        value=";\n".join([
            "Curso principal (1h30)",
            "Exercícios práticos (30min)"
        ]),
        height=100
    )
    plano_estudos[dia] = [a.strip() for a in atividades.split(";") if a.strip()]

# -----------------------------
# GERAR CALENDÁRIO DE ESTUDOS
# -----------------------------
datas_com_atividades = {}
for semana in range(quant_semanas):
    for i, dia in enumerate(dias_semana):
        data_atual = data_inicio + datetime.timedelta(days=(semana * 7) + i)
        data_formatada = data_atual.strftime("%d/%m/%Y")
        titulo = f"{dia} - {data_formatada}"
        datas_com_atividades[titulo] = plano_estudos[dia]

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
