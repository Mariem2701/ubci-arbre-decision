import streamlit as st
from PIL import Image
import os
import uuid
import json


def get_google_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open("ubci_decision_data").sheet1

sheet = get_google_sheet()


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

# Historique visible uniquement par SCI
if service_connecte == "Comptabilité des immobilisations" and st.session_state.history:
    st.markdown("### 📚 Historique des réponses")
    for qid, rep in st.session_state.history:
        qnum = int(qid.replace("Q", ""))
        libelle = libelles_questions.get(qnum, f"Question {qnum}")
        st.markdown(f"- **{libelle}** → **{rep}**")


elif st.session_state.question_number == 2:
    def suite_q02(choix):
        st.session_state.history.append(("Q2", choix))
        sauvegarder()
        go_to_question(15) if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("2️⃣ La dépense concerne-t-elle un bien physique et tangible ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q2")
    if st.button("➡️ Suivant", key="b2"):
        suite_q02(choix)

elif st.session_state.question_number == 3:
    def suite_q03(choix):
        st.session_state.history.append(("Q3", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("3️⃣ Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q3")
    if st.button("➡️ Suivant", key="b3"):
        suite_q03(choix)

elif st.session_state.question_number == 4:
    def suite_q04(choix):
        st.session_state.history.append(("Q4", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("4️⃣ L'entreprise bénéficie-t-elle des avantages économiques futurs du bien ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q4")
    if st.button("➡️ Suivant", key="b4"):
        suite_q04(choix)

elif st.session_state.question_number == 5:
    def suite_q05(choix):
        st.session_state.history.append(("Q5", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("5️⃣ Le coût du bien peut-il être mesuré de manière fiable ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q5")
    if st.button("➡️ Suivant", key="b5"):
        suite_q05(choix)

elif st.session_state.question_number == 6:
    def suite_q06(choix):
        st.session_state.history.append(("Q6", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("6️⃣ Les risques et produits sont-ils transférés à l'entreprise ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q6")
    if st.button("➡️ Suivant", key="b6"):
        suite_q06(choix)

elif st.session_state.question_number == 7:
    def suite_q07(choix):
        st.session_state.history.append(("Q7", choix))
        sauvegarder()
        go_to_question(9) if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("7️⃣ La dépense correspond-elle à des frais d’étude ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q7")
    if st.button("➡️ Suivant", key="b7"):
        suite_q07(choix)

elif st.session_state.question_number == 8:
    def suite_q08(choix):
        st.session_state.history.append(("Q8", choix))
        sauvegarder()
        st.success("✅ Conclusion : Immobilisation corporelle") if choix == "Oui" else st.success("✅ Conclusion : Charge")
    st.markdown("---")
    st.subheader("8️⃣ Les frais d’étude sont-ils directement liés à la constitution d’un actif durable ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q8")
    if st.button("➡️ Suivant", key="b8"):
        suite_q08(choix)

elif st.session_state.question_number == 9:
    def suite_q09(choix):
        st.session_state.history.append(("Q9", choix))
        sauvegarder()
        st.success("✅ Conclusion : Immobilisation corporelle") if choix == "Oui" else next_question()
    st.markdown("---")
    st.subheader("9️⃣ S'agit-il d'une nouvelle acquisition ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q9")
    if st.button("➡️ Suivant", key="b9"):
        suite_q09(choix)

elif st.session_state.question_number == 10:
    def suite_q10(choix):
        st.session_state.history.append(("Q10", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("10️⃣ La valeur vénale de la composante est-elle ≥ 1/4 de la valeur de l'actif ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q10")
    if st.button("➡️ Suivant", key="b10"):
        suite_q10(choix)

elif st.session_state.question_number == 11:
    def suite_q11(choix):
        st.session_state.history.append(("Q11", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("11️⃣ L'actif initial est-il identifié dans SAP comme investissement ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q11")
    if st.button("➡️ Suivant", key="b11"):
        suite_q11(choix)

elif st.session_state.question_number == 12:
    def suite_q12(choix):
        st.session_state.history.append(("Q12", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("12️⃣ Prolonge-t-il la durée de vie ou augmente-t-il la performance de l'actif ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q12")
    if st.button("➡️ Suivant", key="b12"):
        suite_q12(choix)

elif st.session_state.question_number == 13:
    def suite_q13(choix):
        st.session_state.history.append(("Q13", choix))
        sauvegarder()
        st.success("✅ Conclusion : Immobilisation corporelle") if choix == "Réhabilitation majeure" else next_question()
    st.markdown("---")
    st.subheader("13️⃣ S'agit-il d’une réparation ou réhabilitation majeure ?")
    choix = st.radio("Réponse :", ['Réparation', 'Réhabilitation majeure'], key="q13")
    if st.button("➡️ Suivant", key="b13"):
        suite_q13(choix)

elif st.session_state.question_number == 14:
    def suite_q14(choix):
        st.session_state.history.append(("Q14", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("14️⃣ La réparation présente-t-elle un caractère cyclique ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q14")
    if st.button("➡️ Suivant", key="b14"):
        suite_q14(choix)

elif st.session_state.question_number == 15:
    def suite_q15(choix):
        st.session_state.history.append(("Q15", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("15️⃣ L’élément est-il identifiable ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q15")
    if st.button("➡️ Suivant", key="b15"):
        suite_q15(choix)

elif st.session_state.question_number == 16:
    def suite_q16(choix):
        st.session_state.history.append(("Q16", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("16️⃣ Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q16")
    if st.button("➡️ Suivant", key="b16"):
        suite_q16(choix)

elif st.session_state.question_number == 17:
    def suite_q17(choix):
        st.session_state.history.append(("Q17", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("17️⃣ L'entreprise contrôle-t-elle l'élément et en retire-t-elle des avantages économiques futurs probables ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q17")
    if st.button("➡️ Suivant", key="b17"):
        suite_q17(choix)

elif st.session_state.question_number == 18:
    def suite_q18(choix):
        st.session_state.history.append(("Q18", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("18️⃣ Le coût peut-il être mesuré de manière fiable ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q18")
    if st.button("➡️ Suivant", key="b18"):
        suite_q18(choix)

elif st.session_state.question_number == 19:
    def suite_q19(choix):
        st.session_state.history.append(("Q19", choix))
        sauvegarder()
        go_to_question(20) if choix == "Acquisition" else (go_to_question(25) if choix == "Création en interne" else go_to_question(30))
    st.markdown("---")
    st.subheader("19️⃣ S'agit-il d'une acquisition, création en interne ou d'une dépense liée à un actif ?")
    choix = st.radio("Réponse :", ['Acquisition', 'Création en interne', 'Dépense liée à un actif'], key="q19")
    if st.button("➡️ Suivant", key="b19"):
        suite_q19(choix)

elif st.session_state.question_number == 20:
    def suite_q20(choix):
        st.session_state.history.append(("Q20", choix))
        sauvegarder()
        st.success("✅ Conclusion : Immobilisation incorporelle") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("20️⃣ L'acquisition concerne-t-elle une licence ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q20")
    if st.button("➡️ Suivant", key="b20"):
        suite_q20(choix)

elif st.session_state.question_number == 21:
    def suite_q21(choix):
        st.session_state.history.append(("Q21", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("21️⃣ L'actif est-il hébergé sur une infrastructure contrôlée par l'entreprise ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q21")
    if st.button("➡️ Suivant", key="b21"):
        suite_q21(choix)

elif st.session_state.question_number == 22:
    def suite_q22(choix):
        st.session_state.history.append(("Q22", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("22️⃣ L’entreprise dispose-t-elle d’un droit d’usage distinct et exclusif de l'actif ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q22")
    if st.button("➡️ Suivant", key="b22"):
        suite_q22(choix)

elif st.session_state.question_number == 23:
    def suite_q23(choix):
        st.session_state.history.append(("Q23", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("23️⃣ Le droit d’usage est-il permanent (licence perpétuelle) ou à long terme (≥ 3 ans) ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q23")
    if st.button("➡️ Suivant", key="b23"):
        suite_q23(choix)

elif st.session_state.question_number == 24:
    def suite_q24(choix):
        st.session_state.history.append(("Q24", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("24️⃣ Le contrat prévoit-il un abonnement/paiement récurrent ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q24")
    if st.button("➡️ Suivant", key="b24"):
        suite_q24(choix)

elif st.session_state.question_number == 25:
    def suite_q25(choix):
        st.session_state.history.append(("Q25", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Recherche" else next_question()
    st.markdown("---")
    st.subheader("25️⃣ S'agit-il de dépenses de recherche ou de développement ?")
    choix = st.radio("Réponse :", ['Recherche', 'Développement'], key="q25")
    if st.button("➡️ Suivant", key="b25"):
        suite_q25(choix)

elif st.session_state.question_number == 26:
    if service_connecte == "IT / Juridique" or service_connecte == "Comptabilité des immobilisations":
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
            if all(conds):
                st.success("✅ Conclusion : Immobilisation incorporelle")
            else:
                st.success("✅ Conclusion : Charge")
    else:
        st.warning("⛔ Cette question ne concerne pas votre service.")

elif st.session_state.question_number == 27:
    def suite_q27(choix):
        st.session_state.history.append(("Q27", choix))
        sauvegarder()
        next_question()
    st.markdown("---")
    st.subheader("27️⃣ Question 27")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q27")
    if st.button("➡️ Suivant", key="b27"):
        suite_q27(choix)

elif st.session_state.question_number == 28:
    def suite_q28(choix):
        st.session_state.history.append(("Q28", choix))
        sauvegarder()
        next_question()
    st.markdown("---")
    st.subheader("28️⃣ Question 28")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q28")
    if st.button("➡️ Suivant", key="b28"):
        suite_q28(choix)

elif st.session_state.question_number == 29:
    def suite_q29(choix):
        st.session_state.history.append(("Q29", choix))
        sauvegarder()
        next_question()
    st.markdown("---")
    st.subheader("29️⃣ Question 29")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q29")
    if st.button("➡️ Suivant", key="b29"):
        suite_q29(choix)

elif st.session_state.question_number == 30:
    def suite_q30(choix):
        st.session_state.history.append(("Q30", choix))
        sauvegarder()
        go_to_question(32) if choix == "Oui" else go_to_question(31)
    st.markdown("---")
    st.subheader("30️⃣ S'agit-il d'une dépense de maintenance ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q30")
    if st.button("➡️ Suivant", key="b30"):
        suite_q30(choix)

elif st.session_state.question_number == 31:
    def suite_q31(choix):
        st.session_state.history.append(("Q31", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("31️⃣ La dépense est-elle directement attribuable à la préparation de l'actif ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q31")
    if st.button("➡️ Suivant", key="b31"):
        suite_q31(choix)

elif st.session_state.question_number == 32:
    def suite_q32(choix):
        st.session_state.history.append(("Q32", choix))
        sauvegarder()
        go_to_question(34) if choix == "Avant" else go_to_question(33)
    st.markdown("---")
    st.subheader("32️⃣ La dépense est-elle réalisée avant ou après la mise en service de l’actif ?")
    choix = st.radio("Réponse :", ['Avant', 'Après'], key="q32")
    if st.button("➡️ Suivant", key="b32"):
        suite_q32(choix)

elif st.session_state.question_number == 33:
    def suite_q33(choix):
        st.session_state.history.append(("Q33", choix))
        sauvegarder()
        st.success("✅ Conclusion : Immobilisation corporelle") if choix == "Évolutive" else st.success("✅ Conclusion : Charge")
    st.markdown("---")
    st.subheader("33️⃣ La maintenance est-elle évolutive ou corrective ?")
    choix = st.radio("Réponse :", ['Évolutive', 'Corrective'], key="q33")
    if st.button("➡️ Suivant", key="b33"):
        suite_q33(choix)

elif st.session_state.question_number == 34:
    def suite_q34(choix):
        st.session_state.history.append(("Q34", choix))
        sauvegarder()
        st.success("✅ Conclusion : Charge") if choix == "Non" else next_question()
    st.markdown("---")
    st.subheader("34️⃣ Cette dépense est-elle nécessaire pour rendre l’actif opérationnel ?")
    choix = st.radio("Réponse :", ['Oui', 'Non'], key="q34")
    if st.button("➡️ Suivant", key="b34"):
        suite_q34(choix)
# Affichage de l'historique (visible uniquement par la Comptabilité des immobilisations)
if service_connecte == "Comptabilité des immobilisations" and "history" in st.session_state:
    if st.session_state.history:
        st.markdown("### 📚 Historique des réponses")


def enregistrer_reponse(session_id, intitule, description, service, question_id, reponse):
    horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ligne = [session_id, intitule, description, service, question_id, reponse, horodatage]
    try:
        sheet.append_row(ligne)
    except Exception as e:
        st.error(f"Erreur lors de l'enregistrement dans Google Sheets : {e}")

        for qid, rep in st.session_state.history:
            qnum = int(qid.replace("Q", ""))
            libelle = libelles_questions.get(qnum, f"Question {qnum}")
            st.markdown(f"- **{libelle}** → **{rep}**")

