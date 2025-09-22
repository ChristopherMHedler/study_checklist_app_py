README.md para o seu app no Streamlit.
Ele vai explicar o que é, como usar, como configurar o Firebase e também como personalizar as datas e os cursos.

# 📅 Plano de Estudos - Tech + Saúde

Um aplicativo interativo em **Streamlit** para organizar e acompanhar seu plano de estudos na área de **Tecnologia e Saúde**.  
O progresso é salvo automaticamente no **Firebase Realtime Database**, permitindo que você acompanhe suas atividades em qualquer dispositivo.  

👉 Acesse o app online:  
🔗 [Study Checklist App](https://studychecklistapppy-3wyxfbdh4urhmvlnxgvlwz.streamlit.app/#domingo-ate-6h-manha-tarde-noite-28-09-2025)

---

## ✨ Funcionalidades

- ✅ Controle de atividades concluídas  
- 📅 Datas reais no formato **dia/mês/ano**, iniciando da data escolhida  
- 🔄 Geração automática de semanas (você define quantas quer)  
- ✏️ Personalização de cursos e atividades na barra lateral  
- ☁️ Progresso salvo no **Firebase** (não perde ao fechar o app)  

---

## 🚀 Como usar

1. Abra o app no link acima.  
2. Na **barra lateral (à esquerda)**:  
   - Defina a **data de início** do cronograma.  
   - Escolha quantas **semanas** deseja gerar.  
   - Edite os **cursos e atividades** de cada dia da semana.  
3. Marque as caixas de seleção conforme concluir cada atividade.  
4. Clique no botão **💾 Salvar progresso** para guardar no Firebase.  

---

## ⚙️ Configuração do Firebase

Este app usa o **Firebase Realtime Database**.  
Para configurar o seu:

1. Crie um projeto no [Firebase Console](https://console.firebase.google.com).  
2. Vá em **Realtime Database → Criar banco de dados**.  
3. Copie a URL gerada, algo como:  


https://SEU-PROJETO-default-rtdb.firebaseio.com

4. No código, substitua a variável:
```python
FIREBASE_URL = "https://SEU-PROJETO.firebaseio.com"


Defina as regras de leitura e escrita para permitir acesso:

{
  "rules": {
    ".read": true,
    ".write": true
  }
}


(em produção, configure regras seguras com autenticação!)

🛠️ Instalação local (opcional)

Se quiser rodar o projeto na sua máquina:

# Clone este repositório
git clone https://github.com/seu-usuario/plano-estudos.git

# Entre na pasta
cd plano-estudos

# Crie um ambiente virtual (opcional)
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt

# Execute o app
streamlit run app.py

📌 Personalização

Data inicial → escolhida na barra lateral.

Número de semanas → configurável (até 52).

Cursos e atividades → editáveis via campo de texto na barra lateral.

Formato de exportação → pode ser adaptado para gerar planilhas Excel/CSV.

Para rodar o seu app no Streamlit Cloud ou localmente sem problemas, você precisa de um arquivo requirements.txt listando as dependências.

Como seu código usa apenas Streamlit e Requests (e opcionalmente Pandas se quiser exportar planilhas), o arquivo fica simples:

streamlit==1.38.0
requests==2.32.3
pandas==2.2.3

📌 Explicação

streamlit → framework principal do app.

requests → para comunicação com o Firebase.

pandas → já deixei incluído porque pode ser útil caso você queira exportar para Excel/CSV depois.

📊 Exportar cronograma para Excel.

Ele gera um .xlsx com colunas:

Data (dd/mm/yyyy)

Dia (Segunda-feira, Terça, etc)

Atividade

Concluído (✅ ou ❌)

Você pode baixar direto pelo navegador via st.download_button
