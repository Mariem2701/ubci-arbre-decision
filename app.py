import streamlit as st
from PIL import Image
import os
import uuid
import json


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

# Vérification de l'ID de session dans l'URL
query_params = st.query_params
session_id = query_params.get("id", [None])[0]



# Création d'une nouvelle session (par Comptabilité des immo)
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
            st.markdown(f"🔗 Voici le lien à partager :")
            st.code(f"?id={session_id}")
            st.stop()
    else:
        st.error("❌ Aucun ID de session fourni. Veuillez demander un lien à la comptabilité.")
        st.stop()
else:
    # Chargement de la session existante (version robuste)
    filepath = f"data/{session_id}.json"

    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            data = json.load(f)
    else:
        st.error("❌ Lien invalide ou session expirée.")
        st.stop()



# Stockage initial pour intitule/description
data_init = data  # Réutilise le fichier déjà chargé



# Préparation des variables de session à partir du fichier
if 'question_number' not in st.session_state:
    st.session_state.question_number = data.get("question_number", 1)
if 'history' not in st.session_state:
    st.session_state.history = data.get("history", [])


# Bouton réinitialisation
def reset():
    st.session_state.question_number = 1
    st.session_state.history = []

st.sidebar.button("🔄 Réinitialiser", on_click=reset)

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
service_connecte = st.sidebar.selectbox("👤 Connecté en tant que :", services)

# Navigation
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


# Services responsables
services_responsables = {
    1: "Demandeur",
    2: "Comptabilité des immobilisations",
    3: "Demandeur",
    4: "Contrôle de gestion",
    5: "Contrôle de gestion",
    6: "Achats",
    7: "Demandeur",
    8: "Comptabilité des immobilisations",
    9: "Achats",
    10: "Comptabilité des immobilisations",
    11: "IT / Juridique",
    12: "Comptabilité des immobilisations",
    13: "Services Généraux",
    14: "Services Généraux",
    15: "Comptabilité des immobilisations",
    16: "Demandeur",
    17: "Contrôle de gestion",
    18: "Contrôle de gestion",
    19: "Comptabilité des immobilisations",
    20: "IT / Juridique",
    21: "IT",
    22: "IT / Juridique",
    23: "Achats",
    24: "Comptabilité des fournisseurs",
    25: "Comptabilité des immobilisations",
    26: "IT / Juridique",
    30: "IT",
    31: "Comptabilité des fournisseurs",
    32: "IT",
    33: "IT",
    34: "IT",
}

# Fonction pour afficher le service responsable
def afficher_service(question_num):
    service = services_responsables.get(question_num)
    if service:
        st.markdown(f"👤 **Service concerné :** {service}")

# Fonction d'affichage conditionnelle
def afficher_question(num, titre, texte, options, key_radio, bouton_key, suite_callback):
    service_responsable = services_responsables.get(num)
    if service_connecte == service_responsable or service_connecte == "Comptabilité des immobilisations":
        st.markdown("---")
        st.subheader(titre)
        afficher_service(num)
        choix = st.radio(texte, options, key=key_radio)
        if st.button("➡️ Suivant", key=bouton_key):
            st.session_state.history.append((f"Q{num}", choix))
            suite_callback(choix)
    else:
        st.warning("⛔ Cette question ne concerne pas votre service.")

# Mapping des libellés de questions (sans numérotation)
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

# Affichage global des détails de la demande (intitulé + description)
st.markdown("## 📝 Demande en cours")
st.markdown(f"**📌 Intitulé :** {data_init.get('intitule', 'Non renseigné')}")

if data_init.get("description"):
    st.markdown(f"**🗒️ Description :** {data_init.get('description')}")



# Question 1
if st.session_state.question_number == 1:
    def suite_q1(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : Cette dépense est comptabilisée en **Charge**.")
    afficher_question(1, "1️⃣ La dépense est-elle supérieure à 500 DT ?", "Réponse :", ["Oui", "Non"], "q1", "b1", suite_q1)

# Question 2
elif st.session_state.question_number == 2:
    def suite_q2(choix):
        if choix == "Oui":
            next_question()
        else:
            go_to_question(15)
    afficher_question(2, "2️⃣ La dépense concerne-t-elle un bien physique et tangible ?", "Réponse :", ["Oui", "Non"], "q2", "b2", suite_q2)

elif st.session_state.question_number == 3:
    def suite_q3(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(3, "3️⃣ Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?", "Réponse :", ["Oui", "Non"], "q3", "b3", suite_q3)

elif st.session_state.question_number == 4:
    def suite_q4(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(4, "4️⃣ L'entreprise bénéficie-t-elle des avantages économiques futurs du bien ?", "Réponse :", ["Oui", "Non"], "q4", "b4", suite_q4)

elif st.session_state.question_number == 5:
    def suite_q5(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(5, "5️⃣ Le coût du bien peut-il être mesuré de manière fiable ?", "Réponse :", ["Oui", "Non"], "q5", "b5", suite_q5)

elif st.session_state.question_number == 6:
    def suite_q6(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(6, "6️⃣ Les risques et produits sont-ils transférés à l'entreprise ?", "Réponse :", ["Oui", "Non"], "q6", "b6", suite_q6)

elif st.session_state.question_number == 7:
    def suite_q7(choix):
        if choix == "Oui":
            next_question()
        else:
            go_to_question(9)
    afficher_question(7, "7️⃣ La dépense correspond-elle à des frais d’étude ?", "Réponse :", ["Oui", "Non"], "q7", "b7", suite_q7)

elif st.session_state.question_number == 8:
    def suite_q8(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(8, "8️⃣ Les frais d’étude sont-ils directement liés à la constitution d’un actif durable ?", "Réponse :", ["Oui", "Non"], "q8", "b8", suite_q8)

elif st.session_state.question_number == 9:
    def suite_q9(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            next_question()
    afficher_question(9, "9️⃣ S'agit-il d'une nouvelle acquisition ?", "Réponse :", ["Oui", "Non"], "q9", "b9", suite_q9)

# Question 10
elif st.session_state.question_number == 10:
    def suite_q10(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(10, "🔧 1️⃣0️⃣ La valeur vénale de la composante est-elle ≥ 1/4 de la valeur de l'actif ?", "Réponse :", ["Oui", "Non"], "q10", "b10", suite_q10)

# Question 11
elif st.session_state.question_number == 11:
    def suite_q11(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(11, "🔧 1️⃣1️⃣ L'actif initial est-il identifié dans SAP comme investissement ?", "Réponse :", ["Oui", "Non"], "q11", "b11", suite_q11)

# Question 12
elif st.session_state.question_number == 12:
    def suite_q12(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(12, "🔧 1️⃣2️⃣ Prolonge-t-il la durée de vie ou augmente-t-il la performance de l'actif ?", "Réponse :", ["Oui", "Non"], "q12", "b12", suite_q12)

# Question 13
elif st.session_state.question_number == 13:
    def suite_q13(choix):
        if choix == "Réhabilitation majeure":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            next_question()
    afficher_question(13, "🔧 1️⃣3️⃣ S'agit-il d’une réparation ou réhabilitation majeure ?", "Réponse :", ["Réparation", "Réhabilitation majeure"], "q13", "b13", suite_q13)

# Question 14
elif st.session_state.question_number == 14:
    def suite_q14(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(14, "🔧 1️⃣4️⃣ La réparation présente-t-elle un caractère cyclique ?", "Réponse :", ["Oui", "Non"], "q14", "b14", suite_q14)

# Question 15
elif st.session_state.question_number == 15:
    def suite_q15(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(15, "1️⃣5️⃣ L’élément est-il identifiable ?", "(Peut-il être séparé ou découle-t-il de droits légaux ?)", ["Oui", "Non"], "q15", "b15", suite_q15)

# Question 16
elif st.session_state.question_number == 16:
    def suite_q16(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(16, "1️⃣6️⃣ Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?", "", ["Oui", "Non"], "q16", "b16", suite_q16)

# Question 17
elif st.session_state.question_number == 17:
    def suite_q17(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(17, "1️⃣7️⃣ L'entreprise contrôle-t-elle l'élément et en retire-t-elle des avantages économiques futurs probables ?", "", ["Oui", "Non"], "q17", "b17", suite_q17)

# Question 18
elif st.session_state.question_number == 18:
    def suite_q18(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(18, "1️⃣8️⃣ Le coût peut-il être mesuré de manière fiable ?", "", ["Oui", "Non"], "q18", "b18", suite_q18)

# Question 19
elif st.session_state.question_number == 19:
    def suite_q19(choix):
        if choix == "Acquisition":
            go_to_question(20)
        elif choix == "Création en interne":
            go_to_question(25)
        else:
            go_to_question(30)
    afficher_question(19, "1️⃣9️⃣ S'agit-il d'une acquisition, création en interne ou d'une dépense liée à un actif ?", "", ["Acquisition", "Création en interne", "Dépense liée à un actif"], "q19", "b19", suite_q19)

# Question 20
elif st.session_state.question_number == 20:
    def suite_q20(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Immobilisation incorporelle**")
    afficher_question(20, "🔹 L'acquisition concerne-t-elle une licence ?", "", ["Oui", "Non"], "q20", "b20", suite_q20)

# Question 21
elif st.session_state.question_number == 21:
    def suite_q21(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(21, "🔹 L'actif est-il hébergé sur une infrastructure contrôlée par l'entreprise ?", "", ["Oui", "Non"], "q21", "b21", suite_q21)

# Question 22
elif st.session_state.question_number == 22:
    def suite_q22(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(22, "🔹 L’entreprise dispose-t-elle d’un droit d’usage distinct et exclusif de l'actif ?", "", ["Oui", "Non"], "q22", "b22", suite_q22)

# Question 23
elif st.session_state.question_number == 23:
    def suite_q23(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(23, "🔹 Le droit d’usage est-il permanent (licence perpétuelle) ou à long terme (≥ 3 ans) ?", "", ["Oui", "Non"], "q23", "b23", suite_q23)

# Question 24
elif st.session_state.question_number == 24:
    def suite_q24(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Charge**")
        else:
            st.success("✅ Conclusion : **Immobilisation incorporelle**")
    afficher_question(24, "🔹 Le contrat prévoit-il un abonnement/paiement récurrent ?", "", ["Oui", "Non"], "q24", "b24", suite_q24)

# Question 25
elif st.session_state.question_number == 25:
    def suite_q25(choix):
        if choix == "Recherche":
            st.success("✅ Conclusion : **Charge**")
        else:
            next_question()
    afficher_question(25, "🧪 S'agit-il de dépenses de recherche ou de développement ?", "", ["Recherche", "Développement"], "q25", "b25", suite_q25)

# Question 26
elif st.session_state.question_number == 26:
    if service_connecte == services_responsables.get(26) or service_connecte == "Comptabilité des immobilisations":
        st.subheader("🧪 Les conditions IAS 38.57 sont-elles toutes remplies ?")
        afficher_service(26)
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
                st.success("✅ Conclusion : **Immobilisation incorporelle**")
            else:
                st.success("✅ Conclusion : **Charge**")
    else:
        st.warning("⛔ Cette question ne concerne pas votre service.")

# Question 30
elif st.session_state.question_number == 30:
    def suite_q30(choix):
        if choix == "Oui":
            go_to_question(32)
        else:
            go_to_question(31)
    afficher_question(30, "🔧 S'agit-il d'une dépense de maintenance ?", "", ["Oui", "Non"], "q30", "b30", suite_q30)

# Question 31
elif st.session_state.question_number == 31:
    def suite_q31(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(31, "🔧 La dépense est-elle directement attribuable à la préparation de l'actif ?", "", ["Oui", "Non"], "q31", "b31", suite_q31)

# Question 32
elif st.session_state.question_number == 32:
    def suite_q32(choix):
        if choix == "Avant":
            go_to_question(34)
        else:
            go_to_question(33)
    afficher_question(32, "🔧 La dépense est-elle réalisée avant ou après la mise en service de l’actif ?", "", ["Avant", "Après"], "q32", "b32", suite_q32)

# Question 33
elif st.session_state.question_number == 33:
    def suite_q33(choix):
        if choix == "Évolutive":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(33, "🔧 La maintenance est-elle évolutive ou corrective ?", "", ["Évolutive", "Corrective"], "q33", "b33", suite_q33)

# Question 34
elif st.session_state.question_number == 34:
    def suite_q34(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(34, "🔧 Cette dépense est-elle nécessaire pour rendre l’actif opérationnel ?", "", ["Oui", "Non"], "q34", "b34", suite_q34)
