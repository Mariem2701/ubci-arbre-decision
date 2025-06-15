import streamlit as st
from PIL import Image
import uuid
import os
import json
from datetime import datetime



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

# Affichage du contexte de la dépense
if "intitule_depense" in st.session_state:
    with st.expander("📌 Dépense en cours", expanded=True):
        st.markdown(f"**📝 Intitulé :** {st.session_state.intitule_depense}")
        if st.session_state.description_depense:
            st.markdown(f"**📄 Description :** {st.session_state.description_depense}")

# Initialisation
if 'question_number' not in st.session_state:
    st.session_state.question_number = 1
if 'history' not in st.session_state:
    st.session_state.history = []

if 'intitule_depense' not in st.session_state:
    st.session_state.intitule_depense = ""

if 'description_depense' not in st.session_state:
    st.session_state.description_depense = ""

# Lire l'ID du dossier depuis l'URL si présent
params = st.query_params
dossier_id_param = params.get("dossier", [None])[0]


# Charger un dossier existant si un paramètre "dossier" est passé dans l'URL
if dossier_id_param and "dossier_id" not in st.session_state:
    chemin = f"data/{dossier_id_param}.json"
    if os.path.exists(chemin):
        with open(chemin, "r") as f:
            data = json.load(f)
            st.session_state.dossier_id = dossier_id_param
            st.session_state.intitule_depense = data.get("intitule", "")
            st.session_state.description_depense = data.get("description", "")
            st.session_state.history = data.get("reponses", [])

            # Déduire la prochaine question
            if st.session_state.history:
                last_question = st.session_state.history[-1][0]
                try:
                    last_num = int(last_question.replace("Q", ""))
                    st.session_state.question_number = last_num + 1
                except:
                    st.session_state.question_number = 1
            else:
                st.session_state.question_number = 1
    else:
        st.warning("❌ Dossier introuvable.")


# Charger un dossier existant si un paramètre "dossier" est passé dans l'URL
if dossier_id_param:
    chemin = f"data/{dossier_id_param}.json"
    if os.path.exists(chemin):
        with open(chemin, "r") as f:
            data = json.load(f)
            st.session_state.dossier_id = dossier_id_param
            st.session_state.intitule_depense = data.get("intitule", "")
            st.session_state.description_depense = data.get("description", "")
            st.session_state.history = data.get("reponses", [])

            # Déduire la prochaine question à poser (si possible)
            if st.session_state.history:
                last_question = st.session_state.history[-1][0]  # ex : "Q5"
                try:
                    last_num = int(last_question.replace("Q", ""))
                    st.session_state.question_number = last_num + 1
                except:
                    st.session_state.question_number = 1
            else:
                st.session_state.question_number = 1
    else:
        st.warning("❌ Dossier introuvable.")




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


# Blocage uniquement si l’intitulé est vide ET aucun dossier chargé
if not st.session_state.intitule_depense:
    if "dossier_id" not in st.session_state:
        if service_connecte != "Comptabilité des immobilisations":
            st.error("⛔ L’outil est en attente de saisie de l’intitulé de la dépense par la Comptabilité des immobilisations.")
            st.stop()





# Navigation
def next_question():
    st.session_state.question_number += 1

def go_to_question(n):
    st.session_state.question_number = n

def enregistrer_fiche(dossier_id, intitule, description, reponses):
    os.makedirs("data", exist_ok=True)
    with open(f"data/{dossier_id}.json", "w") as f:
        json.dump({
            "intitule": intitule,
            "description": description,
            "reponses": reponses
        }, f)

# Services responsables
services_responsables = {
    1: "Demandeur",
    2: "Comptabilité des immobilisations",

    # Immobilisations corporelles
    3: "Demandeur",
    4: "Contrôle de gestion",
    5: "Contrôle de gestion",
    6: "Achats",
    7: "Demandeur",
    8: "Comptabilité des immobilisations",

    # Grosses réparations
    9: "Achats",
    10: "Comptabilité des immobilisations",
    11: "Contrôle de gestion",
    12: "Comptabilité des immobilisations",
    13: "Services Généraux",

    # Immobilisations incorporelles
    14: "Services Généraux",
    15: "Comptabilité des immobilisations",
    16: "Demandeur",
    17: "Contrôle de gestion",

    # Acquisition
    18: "Comptabilité des immobilisations",

    # Licence
    19: "IT / Juridique",
    20: "Comptabilité des immobilisations",
    21: "IT / Juridique",

    # Logiciel
    22: "IT",
    23: "IT",

    # Droit d’usage
    24: "IT / Juridique",

    # Création en interne
    25: "Comptabilité des immobilisations",
    26: "Comptabilité des immobilisations",

    # Dépenses liées à un actif
    27: "Comptabilité des immobilisations",
    28: "Comptabilité des immobilisations",
    29: "IT",
    30: "IT",
}


# Fonction pour afficher le service responsable
def afficher_service(question_num):
    service = services_responsables.get(question_num)
    if service:
        st.markdown(f"👤 **Service concerné :** {service}")

if service_connecte == "Comptabilité des immobilisations" and st.session_state.question_number == 1:
    st.markdown("### 📝 Informations sur la dépense")

    # Génère un ID unique une seule fois
    if "dossier_id" not in st.session_state:
        st.session_state.dossier_id = str(uuid.uuid4())[:6]

    st.session_state.intitule_depense = st.text_input("**Intitulé de la dépense** (obligatoire)", st.session_state.intitule_depense)
    st.session_state.description_depense = st.text_area("**Description** (facultatif)", st.session_state.description_depense)

    if not st.session_state.intitule_depense:
        st.warning("⚠️ Veuillez saisir l’intitulé de la dépense avant de continuer.")
        st.stop()

  
# 📎 Afficher lien à partager si dossier_id existe
if "dossier_id" in st.session_state:
    base_url = "https://ubci-arbre-decision-nzgmblwykw3dwkekw2dzwt.streamlit.app"
    lien = f"{base_url}/?dossier={st.session_state.dossier_id}"

    st.markdown("🔗 **Lien à partager :**")
    st.text_input("URL à copier", value=lien, label_visibility="collapsed")




libelles_questions = {
    1: "La dépense est-elle supérieure à 500 DT ?",
    2: "La dépense concerne-t-elle un bien physique et tangible ?",

    # Immobilisations corporelles
    3: "Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?",
    4: "L'entreprise bénéficie-t-elle des avantages économiques futurs du bien ?",
    5: "Le coût du bien peut-il être mesuré de manière fiable ?",
    6: "La dépense correspond-elle à des frais d’étude ?",
    7: "Les frais d’étude sont-ils directement liés à la constitution d’un actif durable ?",
    8: "S'agit-il d'une nouvelle acquisition ?",

    # Grosse réparation
    9: "L’actif initial est-il identifié dans SAP en tant qu’investissement ?",
    10: "La valeur vénale de la composante est-elle ≥ 1/4 de la valeur de l’actif ?",
    11: "Prolonge-t-il la durée de vie de l’élément ou en augmente-t-il la performance ?",
    12: "S’agit-il d’une réparation ou d’un renouvellement cyclique d’une composante essentielle ?",
    13: "S'agit-il d'une panne imprévue liée à un bien totalement amorti ou nouvellement acquis ?",

    # Immobilisations incorporelles
    14: "Est-il destiné à être utilisé pour plus d’un exercice (> 1 an) ?",
    15: "L'entreprise contrôle-t-elle l'élément et en retire-t-elle des avantages économiques futurs probables ?",
    16: "Le coût peut-il être mesuré de manière fiable ?",
    17: "S'agit-il d'une acquisition, création en interne ou d'une dépense liée à un actif ?",

    # Acquisition sous-branches
    18: "L’acquisition concerne-t-elle une licence, un logiciel ou un droit d’usage ?",

    # Sous-branche licence
    19: "L’entreprise dispose-t-elle d’un droit d’usage distinct et exclusif de l'actif ?",
    20: "La licence est-elle perpétuelle ou accordée pour une longue période (≥ 3 ans) ?",
    21: "Le contrat prévoit-il un abonnement, une redevance ou un paiement récurrent ?",

    # Sous-branche logiciels
    22: "Le logiciel est-il intégré à un matériel sans valeur autonome (ex. firmware, OS embarqué) ?",
    23: "La licence associée est-elle perpétuelle ou accordée pour une durée longue (≥ 3 ans) ?",

    # Sous-branche droit d’usage
    24: "Le droit d’usage est-il limité dans le temps, sans transfert de contrôle ?",

    # Création en interne
    25: "S'agit-il de dépenses de recherche ou de développement ?",
    26: "Les conditions IAS 38.57 sont-elles toutes remplies ?",

    # Dépense liée à un actif
    27: "S'agit-il d'une dépense récurrente (maintenance) ?",
    28: "La dépense est-elle directement attribuable à la préparation de l'actif en vue de son utilisation ?",
    29: "La dépense est-elle réalisée avant ou après la mise en service de l’actif ?",
    30: "La dépense concerne-t-elle une maintenance évolutive ou corrective ?"
}


# Affichage historique si "Comptabilité des immobilisations":
if service_connecte == "Comptabilité des immobilisations":
    with st.expander("📋 Suivi de l’avancement des réponses"):
        for question_key, reponse in st.session_state.history:
            num = int(question_key.replace("Q", ""))
            texte = libelles_questions.get(num, f"Question {num}")
            st.markdown(f"**{texte}**\n➡️ Réponse : `{reponse}`")


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

            # Enregistrement local
            enregistrer_fiche(
                st.session_state.dossier_id,
                st.session_state.intitule_depense,
                st.session_state.description_depense,
                st.session_state.history
            )

        
            suite_callback(choix)
    else:
        st.warning("⛔ Cette question ne concerne pas votre service.")




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
            go_to_question(3)
        else:
            go_to_question(14)
    afficher_question(2, "2️⃣ La dépense concerne-t-elle un bien physique et tangible ?", "Réponse :", ["Oui", "Non"], "q2", "b2", suite_q2)

elif st.session_state.question_number == 3:
    def suite_q3(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : Cette dépense est comptabilisée en **Charge**.")
    afficher_question(3, "3️⃣ Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?", "Réponse :", ["Oui", "Non"], "q3", "b3", suite_q3)


elif st.session_state.question_number == 4:
    def suite_q4(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : Cette dépense est comptabilisée en **Charge**.")
    afficher_question(4, "4️⃣ L'entreprise bénéficie-t-elle des avantages économiques futurs du bien ?", "Réponse :", ["Oui", "Non"], "q4", "b4", suite_q4)


elif st.session_state.question_number == 5:
    def suite_q5(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : Cette dépense est comptabilisée en **Charge**.")
    afficher_question(5, "5️⃣ Le coût du bien peut-il être mesuré de manière fiable ?", "Réponse :", ["Oui", "Non"], "q5", "b5", suite_q5)


elif st.session_state.question_number == 6:
    def suite_q6(choix):
        if choix == "Oui":
            go_to_question(7)
        else:
            go_to_question(8)
    afficher_question(6, "6️⃣ La dépense correspond-elle à des frais d’étude ?", "Réponse :", ["Oui", "Non"], "q6", "b6", suite_q6)


elif st.session_state.question_number == 7:
    def suite_q7(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(7, "7️⃣ Les frais d’étude sont-ils directement liés à un actif durable ?", "Réponse :", ["Oui", "Non"], "q7", "b7", suite_q7)


elif st.session_state.question_number == 8:
    def suite_q8(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            go_to_question(9)
    afficher_question(8, "8️⃣ S'agit-il d'une nouvelle acquisition ?", "Réponse :", ["Oui", "Non"], "q8", "b8", suite_q8)


elif st.session_state.question_number == 9:
    def suite_q9(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(9, "9️⃣ L’actif initial est-il identifié dans SAP en tant qu’investissement ?", "Réponse :", ["Oui", "Non"], "q9", "b9", suite_q9)


elif st.session_state.question_number == 10:
    def suite_q10(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(10, "🔟 La valeur vénale de la composante est-elle ≥ 1/4 de la valeur de l’actif ?", "Réponse :", ["Oui", "Non"], "q10", "b10", suite_q10)


elif st.session_state.question_number == 11:
    def suite_q11(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(11, "1️⃣1️⃣ Prolonge-t-il la durée de vie ou augmente-t-il la performance de l’élément ?", "Réponse :", ["Oui", "Non"], "q11", "b11", suite_q11)


elif st.session_state.question_number == 12:
    def suite_q12(choix):
        if choix == "Réhabilitation majeure":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            go_to_question(13)
    afficher_question(12, "1️⃣2️⃣ S’agit-il d’une réparation ou du renouvellement cyclique d’une composante essentielle ?", "Réponse :", ["Réparation", "Réhabilitation majeure"], "q12", "b12", suite_q12)


elif st.session_state.question_number == 13:
    def suite_q13(choix):
        if choix == "Totalement amorti":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(13, "1️⃣3️⃣ S'agit-il d'une panne imprévue liée à un bien totalement amorti ou nouvellement acquis ?", "Réponse :", ["Totalement amorti", "Nouvellement acquis"], "q13", "b13", suite_q13)

# Question 14
elif st.session_state.question_number == 14:
    def suite_q14(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(14, "1️⃣4️⃣ Est-il destiné à être utilisé pour plus d’un exercice (> 1 an) ?", "Réponse :", ["Oui", "Non"], "q14", "b14", suite_q14)


# Question 15
elif st.session_state.question_number == 15:
    def suite_q15(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(15, "1️⃣5️⃣ L'entreprise contrôle-t-elle l'élément et en retire-t-elle des avantages économiques futurs probables ?", "Réponse :", ["Oui", "Non"], "q15", "b15", suite_q15)


# Question 16
elif st.session_state.question_number == 16:
    def suite_q16(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(16, "1️⃣6️⃣ Le coût peut-il être mesuré de manière fiable ?", "Réponse :", ["Oui", "Non"], "q16", "b16", suite_q16)

# Question 17
elif st.session_state.question_number == 17:
    def suite_q17(choix):
        if choix == "Acquisition":
            go_to_question(18)
        elif choix == "Création en interne":
            go_to_question(25)
        else:
            go_to_question(27)
    afficher_question(17, "1️⃣7️⃣ S'agit-il d'une acquisition, création en interne ou d'une dépense liée à un actif ?", "Réponse :", ["Acquisition", "Création en interne", "Dépense liée à un actif"], "q17", "b17", suite_q17)


# Question 18
elif st.session_state.question_number == 18:
    def suite_q18(choix):
        if choix == "Licence":
            go_to_question(19)
        elif choix == "Logiciel":
            go_to_question(22)
        else:
            go_to_question(24)
    afficher_question(18, "1️⃣8️⃣ L’acquisition concerne-t-elle une licence, un logiciel ou un droit d’usage ?", "Réponse :", ["Licence", "Logiciel", "Droit d’usage"], "q18", "b18", suite_q18)


# Question 19
elif st.session_state.question_number == 19:
    def suite_q19(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(19, "🔹 L’entreprise dispose-t-elle d’un droit d’usage distinct et exclusif de l'actif ?", "Réponse :", ["Oui", "Non"], "q19", "b19", suite_q19)


# Question 20
elif st.session_state.question_number == 20:
    def suite_q20(choix):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(20, "🔹 La licence est-elle perpétuelle ou accordée pour une longue période (≥ 3 ans) ?", "Réponse :", ["Oui", "Non"], "q20", "b20", suite_q20)


# Question 21
elif st.session_state.question_number == 21:
    def suite_q21(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Charge**")
        else:
            st.success("✅ Conclusion : **Immobilisation incorporelle**")
    afficher_question(21, "🔹 Le contrat prévoit-il un abonnement, une redevance ou un paiement récurrent ?", "Réponse :", ["Oui", "Non"], "q21", "b21", suite_q21)


# Question 22
elif st.session_state.question_number == 22:
    def suite_q22(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            next_question()
    afficher_question(22, "🔹 Le logiciel est-il intégré à un matériel sans valeur autonome (ex. firmware, OS embarqué) ?", "Réponse :", ["Oui", "Non"], "q22", "b22", suite_q22)


# Question 23
elif st.session_state.question_number == 23:
    def suite_q23(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation incorporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(23, "🔹 La licence associée est-elle perpétuelle ou ≥ 3 ans ?", "Réponse :", ["Oui", "Non"], "q23", "b23", suite_q23)


# Question 24
elif st.session_state.question_number == 24:
    def suite_q24(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Charge**")
        else:
            st.success("✅ Conclusion : **Immobilisation incorporelle**")
    afficher_question(24, "🔹 Le droit d’usage est-il limité dans le temps, sans transfert de contrôle ?", "Réponse :", ["Oui", "Non"], "q24", "b24", suite_q24)


# Question 25
elif st.session_state.question_number == 25:
    def suite_q25(choix):
        if choix == "Recherche":
            st.success("✅ Conclusion : **Charge**")
        else:
            next_question()
    afficher_question(25, "🧪 S'agit-il de dépenses de recherche ou de développement ?", "Réponse :", ["Recherche", "Développement"], "q25", "b25", suite_q25)

# Question 26
elif st.session_state.question_number == 26:
    if service_connecte == services_responsables.get(26) or service_connecte == "Comptabilité des immobilisations":
        st.subheader("🧪 Les conditions IAS 38.57 sont-elles toutes remplies ?")
        afficher_service(26)
        conditions = [
            st.checkbox("Faisabilité technique", key="ias1"),
            st.checkbox("Intention d’achever le projet", key="ias2"),
            st.checkbox("Capacité à utiliser ou vendre l'actif", key="ias3"),
            st.checkbox("Avantages économiques futurs probables", key="ias4"),
            st.checkbox("Ressources disponibles", key="ias5"),
            st.checkbox("Dépenses évaluées de façon fiable", key="ias6")
        ]
        if st.button("➡️ Suivant", key="b26"):
            if all(conditions):
                st.success("✅ Conclusion : **Immobilisation incorporelle**")
            else:
                st.success("✅ Conclusion : **Charge**")
    else:
        st.warning("⛔ Cette question ne concerne pas votre service.")

# Question 27
elif st.session_state.question_number == 27:
    def suite_q27(choix):
        if choix == "Oui":
            go_to_question(29)
        else:
            go_to_question(28)
    afficher_question(27, "🔧 S'agit-il d'une dépense récurrente (maintenance) ?", "Réponse :", ["Oui", "Non"], "q27", "b27", suite_q27)


# Question 28
elif st.session_state.question_number == 28:
    def suite_q28(choix):
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(
        28,
        "🔧 La dépense est-elle directement attribuable à la préparation de l'actif en vue de son utilisation ?",
        "Exemples : coûts du personnel, honoraires, tests...",
        ["Oui", "Non"],
        "q28",
        "b28",
        suite_q28
    )


# Question 29
elif st.session_state.question_number == 29:
    def suite_q29(choix):
        if choix == "Avant":
            st.success("✅ Conclusion : **Immobilisation incorporelle**")
        else:
            next_question()
    afficher_question(
        29,
        "🔧 La dépense est-elle réalisée avant ou après la mise en service de l’actif ?",
        "Réponse :",
        ["Avant", "Après"],
        "q29",
        "b29",
        suite_q29
    )


# Question 30
elif st.session_state.question_number == 30:
    def suite_q30(choix):
        if choix == "Évolutive":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")
    afficher_question(
        30,
        "🔧 La maintenance est-elle évolutive ou corrective ?",
        "Évolutive = amélioration / adaptation\nCorrective = réparation du fonctionnement initial",
        ["Évolutive", "Corrective"],
        "q30",
        "b30",
        suite_q30
    )


