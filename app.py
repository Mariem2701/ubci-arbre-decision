import streamlit as st
from PIL import Image
import os
import uuid
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime


def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open("ubci_decision_data").sheet1

sheet = get_google_sheet()


def enregistrer_reponse(session_id, intitule, description, service, question_id, reponse):
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ligne = [session_id, intitule, description, service, question_id, reponse, horodatage]
    try:
        sheet.append_row(ligne)
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement dans Google Sheets : {e}")


# Services disponibles
services = [
    "Demandeur",
    "Comptabilité des immobilisations",
    "Fournisseurs / Comptabilité",
    "Achats",
    "Contrôle de gestion",
    "IT / Juridique",
    "Services Généraux",
    "RH"
]

# Configuration de la page
st.set_page_config(page_title="UBCI - Arbre de Décision Immobilisation", layout="centered")

# Affichage du logo
try:
    logo = Image.open("./ubci_logo.png")
    st.image(logo, width=150)
except FileNotFoundError:
    st.warning("⚠️ Logo non trouvé. Vérifiez que 'ubci_logo.png' est bien dans le dossier du projet.")

st.title("🔍 Arbre de Décision - Traitement des Dépenses (Banque UBCI)")
st.markdown("Bienvenue dans l'outil interactif d’aide à la décision pour la classification des dépenses selon les normes de la Banque **UBCI**.")

service_connecte = st.sidebar.selectbox("👤 Connecté en tant que :", services)

# Initialisation sécurisée de session_state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'question_number' not in st.session_state:
    st.session_state.question_number = 1

# Vérification de l'ID de session dans l'URL
query_params = st.query_params
session_id = query_params.get("id", [None])[0]
data_init = {}

# Création d'une nouvelle session
if not session_id:
    if service_connecte == "Comptabilité des immobilisations":
        st.header("Créer une nouvelle demande")
        intitule = st.text_input("Intitulé de la dépense")
        description = st.text_area("Description (optionnelle)")
        if st.button("🎯 Créer la demande"):
            session_id = str(uuid.uuid4())
            data = {
                "intitule": intitule,
                "description": description,
                "history": [],
                "question_number": 1
            }
            os.makedirs("data", exist_ok=True)
            with open(f"data/{session_id}.json", "w") as f:
                json.dump(data, f)
            st.success("✅ Demande créée !")
            st.markdown("🔗 Voici le lien à partager :")
            st.code(f"?id={session_id}")
            st.stop()
    else:
        st.error("❌ Aucun ID de session fourni. Veuillez demander un lien à la comptabilité.")
        st.stop()
else:
    filepath = f"data/{session_id}.json"
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
        data_init.update(data)
        st.session_state.question_number = data.get("question_number", 1)
        st.session_state.history = data.get("history", [])
    else:
        st.error("❌ Lien invalide ou session expirée.")
        st.stop()

# Fonction pour réinitialiser
st.sidebar.button("🔄 Réinitialiser", on_click=lambda: (st.session_state.update({"question_number": 1, "history": []})))


def next_question():
    st.session_state.question_number += 1


def go_to_question(n):
    st.session_state.question_number = n


def sauvegarder():
    data = {
        "intitule": data_init.get("intitule", ""),
        "description": data_init.get("description", ""),
        "history": st.session_state.history,
        "question_number": st.session_state.question_number
    }
    with open(f"data/{session_id}.json", "w") as f:
        json.dump(data, f)

    if st.session_state.history:
        last_qid, last_rep = st.session_state.history[-1]
        enregistrer_reponse(
            session_id,
            data.get("intitule", ""),
            data.get("description", ""),
            service_connecte,
            last_qid,
            last_rep
        )


# Chargement des questions
libelles_questions = {
    1: "La dépense est-elle supérieure à 500 DT ?",
    2: "La dépense concerne-t-elle un bien physique et tangible ?",
    3: "Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?",
    4: "L'entreprise bénéficie-t-elle des avantages économiques futurs du bien ?",
    5: "Le coût du bien peut-il être mesuré de manière fiable ?",
    6: "Les risques et produits sont-ils transférés à l'entreprise ?",
    7: "La dépense correspond-elle à des frais d’étude ?",
    8: "Les frais d’étude sont-ils directement liés à la constitution d’un actif durable ?",
    9: "S'agit-il d'une nouvelle acquisition ?",
    10: "La valeur vénale de la composante est-elle ≥ 1/4 de la valeur de l'actif ?",
    11: "L'actif initial est-il identifié dans SAP comme investissement ?",
    12: "Prolonge-t-il la durée de vie ou augmente-t-il la performance de l'actif ?",
    13: "S'agit-il d’une réparation ou réhabilitation majeure ?",
    14: "La réparation présente-t-elle un caractère cyclique ?",
    15: "L’élément est-il identifiable ?",
    16: "Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?",
    17: "L'entreprise contrôle-t-elle l'élément et en retire-t-elle des avantages économiques futurs probables ?",
    18: "Le coût peut-il être mesuré de manière fiable ?",
    19: "S'agit-il d'une acquisition, création en interne ou d'une dépense liée à un actif ?",
    20: "L'acquisition concerne-t-elle une licence ?",
    21: "L'actif est-il hébergé sur une infrastructure contrôlée par l'entreprise ?",
    22: "L’entreprise dispose-t-elle d’un droit d’usage distinct et exclusif de l'actif ?",
    23: "Le droit d’usage est-il permanent (licence perpétuelle) ou à long terme (≥ 3 ans) ?",
    24: "Le contrat prévoit-il un abonnement/paiement récurrent ?",
    25: "S'agit-il de dépenses de recherche ou de développement ?",
    26: "Les conditions IAS 38.57 sont-elles toutes remplies ?",
    27: "Cette dépense est-elle soumise à une approbation réglementaire ?",
    28: "Y a-t-il un impact sur les états financiers ?",
    29: "La dépense est-elle liée à un projet stratégique ?",
    30: "S'agit-il d'une dépense de maintenance ?",
    31: "La dépense est-elle directement attribuable à la préparation de l'actif ?",
    32: "La dépense est-elle réalisée avant ou après la mise en service de l’actif ?",
    33: "La maintenance est-elle évolutive ou corrective ?",
    34: "Cette dépense est-elle nécessaire pour rendre l’actif opérationnel ?",
}

# Affichage des données
st.markdown("## 📝 Demande en cours")
st.markdown(f"**📌 Intitulé :** {data_init.get('intitule', 'Non renseigné')}")
if data_init.get("description"):
    st.markdown(f"**🗒️ Description :** {data_init.get('description')}")

if service_connecte == "Comptabilité des immobilisations" and st.session_state.history:
    st.markdown("### 📚 Historique des réponses")
    for qid, rep in st.session_state.history:
        qnum = int(qid.replace("Q", ""))
        libelle = libelles_questions.get(qnum, f"Question {qnum}")
        st.markdown(f"- **{libelle}** → **{rep}**")


# Bloc pour la question 1 (spécial car pas dans la boucle)
if st.session_state.question_number == 1:
    st.markdown("---")
    st.subheader("1️⃣ La dépense est-elle supérieure à 500 DT ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q1")
    if st.button("➡️ Suivant", key="b1"):
        st.session_state.history.append(("Q1", choix))
        sauvegarder()
        if choix == "Non":
            st.success("✅ Conclusion : Charge")
        else:
            next_question()

# Q26 spéciale (checkboxes)
elif st.session_state.question_number == 26:
    if service_connecte in ["IT / Juridique", "Comptabilité des immobilisations"]:
        st.subheader("🧪 Les conditions IAS 38.57 sont-elles toutes remplies ?")
        conds = [
            st.checkbox("Faisabilité technique", key="cond1"),
            st.checkbox("Intention d’achever le projet", key="cond2"),
            st.checkbox("Capacité à utiliser ou vendre l'actif", key="cond3"),
            st.checkbox("Avantages économiques futurs probables", key="cond4"),
            st.checkbox("Ressources disponibles", key="cond5"),
            st.checkbox("Dépenses évaluées de façon fiable", key="cond6")
        ]
        if st.button("➡️ Suivant", key="b26"):
            choix = "Oui" if all(conds) else "Non"
            st.session_state.history.append(("Q26", choix))
            sauvegarder()
            st.success("✅ Conclusion : Immobilisation incorporelle" if choix == "Oui" else "✅ Conclusion : Charge")
    else:
        st.warning("⛔ Cette question ne concerne pas votre service.")

# Blocs interactifs Q2 à Q34 (hors Q26)
else:
    def handle_response(choice, qid):
        st.session_state.history.append((f"Q{qid}", choice))
        sauvegarder()
        next_question()

    for q_num in list(range(2, 26)) + list(range(27, 35)):
        if q_num == st.session_state.question_number:
            st.markdown("---")
            st.subheader(f"{q_num}️⃣ {libelles_questions[q_num]}")

            if q_num == 13:
                choice = st.radio("Réponse :", ['Réparation', 'Réhabilitation majeure'], key=f"q{q_num}")
            elif q_num == 25:
                choice = st.radio("Réponse :", ['Recherche', 'Développement'], key=f"q{q_num}")
            elif q_num == 32:
                choice = st.radio("Réponse :", ['Avant', 'Après'], key=f"q{q_num}")
            elif q_num == 33:
                choice = st.radio("Réponse :", ['Évolutive', 'Corrective'], key=f"q{q_num}")
            else:
                choice = st.radio("Réponse :", ['Oui', 'Non'], key=f"q{q_num}")

            if st.button("➡️ Suivant", key=f"b{q_num}"):
                handle_response(choice, q_num)


        for qid, rep in st.session_state.history:
            qnum = int(qid.replace("Q", ""))
            libelle = libelles_questions.get(qnum, f"Question {qnum}")
            st.markdown(f"- **{libelle}** → **{rep}**")

