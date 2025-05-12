import streamlit as st

# Configuration de la page
st.set_page_config(page_title="UBCI - Arbre de Décision Immobilisation", layout="centered")

# Titre principal
st.title("🔍 Arbre de Décision - Traitement des Dépenses (Banque UBCI)")
st.markdown("Bienvenue dans l'outil interactif d’aide à la décision pour la classification des dépenses selon les normes de la Banque **UBCI**.")

# Initialisation de la session
if 'question_number' not in st.session_state:
    st.session_state.question_number = 1
if 'history' not in st.session_state:
    st.session_state.history = []

# Fonction de navigation
def next_question():
    st.session_state.question_number += 1

def go_to_question(n):
    st.session_state.question_number = n


def reset():
    st.session_state.question_number = 1
    st.session_state.history = []

# Bouton pour recommencer depuis le début
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
service_connecte = st.selectbox("👤 Connecté en tant que :", services)

# Dictionnaire des services responsables par question
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

# Initialisation de la session
if 'question_number' not in st.session_state:
    st.session_state.question_number = 1
if 'history' not in st.session_state:
    st.session_state.history = []

# Navigation
def next_question():
    st.session_state.question_number += 1

def go_to_question(n):
    st.session_state.question_number = n

def reset():
    st.session_state.question_number = 1
    st.session_state.history = []

st.sidebar.button("🔄 Réinitialiser", on_click=reset)

# Fonction d'affichage du service responsable
def afficher_service(question_num):
    service = services_responsables.get(question_num)
    if service:
        st.markdown(f"👤 **Service concerné :** {service}")

# Exemple d'affichage d'une question avec le service concerné
if st.session_state.question_number == 1:
    st.subheader("1️⃣ La dépense est-elle supérieure à 500 DT ?")
    afficher_service(1)
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q1")
    if st.button("➡️ Suivant"):
        st.session_state.history.append(("Q1", choix))
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : Cette dépense est comptabilisée en **Charge**.")

if st.session_state.question_number == 2:
    st.subheader("2️⃣ La dépense concerne-t-elle un bien physique et tangible ?")
    afficher_service(2)
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q2")
    if st.button("➡️ Suivant", key="b2"):
        st.session_state.history.append(("Q2", choix))
        if choix == "Oui":
            next_question()
        else:
            go_to_question(15)

# Question 3
elif st.session_state.question_number == 3:
    st.subheader("3️⃣ Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q3")
    if st.button("➡️ Suivant", key="b3"):
        st.session_state.history.append(("Q3", choix))
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

# Question 4
elif st.session_state.question_number == 4:
    st.subheader("4️⃣ L'entreprise bénéficie-t-elle des avantages économiques futurs du bien ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q4")
    if st.button("➡️ Suivant", key="b4"):
        st.session_state.history.append(("Q4", choix))
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

# Question 5
elif st.session_state.question_number == 5:
    st.subheader("5️⃣ Le coût du bien peut-il être mesuré de manière fiable ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q5")
    if st.button("➡️ Suivant", key="b5"):
        st.session_state.history.append(("Q5", choix))
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

# Question 6
elif st.session_state.question_number == 6:
    st.subheader("6️⃣ Les risques et produits sont-ils transférés à l'entreprise ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q6")
    if st.button("➡️ Suivant", key="b6"):
        st.session_state.history.append(("Q6", choix))
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

# Question 7
elif st.session_state.question_number == 7:
    st.subheader("7️⃣ La dépense correspond-elle à des frais d’étude ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q7")

    if st.button("➡️ Suivant", key="b7"):
        st.session_state.history.append(("Q7", choix))
        if choix == "Oui":
            next_question()  # aller à Q8
        else:
            st.session_state.question_number = 9  # aller directement à Q9


# Question 8 - Frais d’étude
elif st.session_state.question_number == 8:
    st.subheader("8️⃣ Les frais d’étude sont-ils directement liés à la constitution d’un actif durable ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q8")
    if st.button("➡️ Suivant", key="b8"):
        st.session_state.history.append(("Q8", choix))
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")

# Question 9 - Nouvelle acquisition ?
elif st.session_state.question_number == 9:
    st.subheader("9️⃣ S'agit-il d'une nouvelle acquisition ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q9")
    if st.button("➡️ Suivant", key="b9"):
        st.session_state.history.append(("Q9", choix))
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            next_question()

# Question 10 - Grosse réparation
elif st.session_state.question_number == 10:
    st.subheader("🔧 10️⃣ La valeur vénale de la composante est-elle ≥ 1/4 de la valeur de l'actif ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q10")
    if st.button("➡️ Suivant", key="b10"):
        st.session_state.history.append(("Q10", choix))
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

# Question 11
elif st.session_state.question_number == 11:
    st.subheader("🔧 11️⃣ L'actif initial est-il identifié dans SAP comme investissement ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q11")
    if st.button("➡️ Suivant", key="b11"):
        st.session_state.history.append(("Q11", choix))
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

# Question 12
elif st.session_state.question_number == 12:
    st.subheader("🔧 12️⃣ Prolonge-t-il la durée de vie ou augmente-t-il la performance de l'actif ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q12")
    if st.button("➡️ Suivant", key="b12"):
        st.session_state.history.append(("Q12", choix))
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

# Question 13
elif st.session_state.question_number == 13:
    st.subheader("🔧 13️⃣ S'agit-il d’une réparation ou réhabilitation majeure ?")
    choix = st.radio("Réponse :", ["Réparation", "Réhabilitation majeure"], key="q13")
    if st.button("➡️ Suivant", key="b13"):
        st.session_state.history.append(("Q13", choix))
        if choix == "Réhabilitation majeure":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            next_question()

# Question 14
elif st.session_state.question_number == 14:
    st.subheader("🔧 14️⃣ La réparation présente-t-elle un caractère cyclique ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q14")
    if st.button("➡️ Suivant", key="b14"):
        st.session_state.history.append(("Q14", choix))
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")


# Questions incorporelles
elif st.session_state.question_number == 15:
    st.subheader("1️⃣5️⃣ L’élément est-il identifiable ?")
    choix = st.radio("(Peut-il être séparé ou découle-t-il de droits légaux ?)", ["Oui", "Non"], key="q15")
    if st.button("➡️ Suivant", key="b15"):
        st.session_state.history.append(("Q15", choix))
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

elif st.session_state.question_number == 16:
    st.subheader("1️⃣6️⃣ Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?")
    choix = st.radio("", ["Oui", "Non"], key="q16")
    if st.button("➡️ Suivant", key="b16"):
        st.session_state.history.append(("Q16", choix))
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

elif st.session_state.question_number == 17:
    st.subheader("1️⃣7️⃣ L'entreprise contrôle-t-elle l'élément et en retire-t-elle des avantages économiques futurs probables ?")
    choix = st.radio("", ["Oui", "Non"], key="q17")
    if st.button("➡️ Suivant", key="b17"):
        st.session_state.history.append(("Q17", choix))
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

elif st.session_state.question_number == 18:
    st.subheader("1️⃣8️⃣ Le coût peut-il être mesuré de manière fiable ?")
    choix = st.radio("", ["Oui", "Non"], key="q18")
    if st.button("➡️ Suivant", key="b18"):
        st.session_state.history.append(("Q18", choix))
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

elif st.session_state.question_number == 19:
    st.subheader("1️⃣9️⃣ S'agit-il d'une acquisition, création en interne ou d'une dépense liée à un actif ?")
    choix = st.radio("", ["Acquisition", "Création en interne", "Dépense liée à un actif"], key="q19")
    if st.button("➡️ Suivant", key="b19"):
        st.session_state.history.append(("Q19", choix))
        if choix == "Acquisition":
            go_to_question(20)
        elif choix == "Création en interne":
            go_to_question(25)
        else:
            go_to_question(30)

# Branche Acquisition
elif st.session_state.question_number == 20:
    st.subheader("🔹 L'acquisition concerne-t-elle une licence ?")
    choix = st.radio("", ["Oui", "Non"], key="q20")
    if st.button("➡️ Suivant", key="b20"):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Immobilisation incorporelle**")

elif st.session_state.question_number == 21:
    st.subheader("🔹 L'actif est-il hébergé sur une infrastructure contrôlée par l'entreprise ?")
    choix = st.radio("", ["Oui", "Non"], key="q21")
    if st.button("➡️ Suivant", key="b21"):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

elif st.session_state.question_number == 22:
    st.subheader("🔹 L’entreprise dispose-t-elle d’un droit d’usage distinct et exclusif de l'actif ?")
    choix = st.radio("", ["Oui", "Non"], key="q22")
    if st.button("➡️ Suivant", key="b22"):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

elif st.session_state.question_number == 23:
    st.subheader("🔹 Le droit d’usage est-il permanent (licence perpétuelle) ou à long terme (≥ 3 ans) ?")
    choix = st.radio("", ["Oui", "Non"], key="q23")
    if st.button("➡️ Suivant", key="b23"):
        if choix == "Oui":
            next_question()
        else:
            st.success("✅ Conclusion : **Charge**")

elif st.session_state.question_number == 24:
    st.subheader("🔹 Le contrat prévoit-il un abonnement/paiement récurrent ?")
    choix = st.radio("", ["Oui", "Non"], key="q24")
    if st.button("➡️ Suivant", key="b24"):
        if choix == "Oui":
            st.success("✅ Conclusion : **Charge**")
        else:
            st.success("✅ Conclusion : **Immobilisation incorporelle**")

# Branche Création Interne
elif st.session_state.question_number == 25:
    st.subheader("🧪 S'agit-il de dépenses de recherche ou de développement ?")
    choix = st.radio("", ["Recherche", "Développement"], key="q25")
    if st.button("➡️ Suivant", key="b25"):
        if choix == "Recherche":
            st.success("✅ Conclusion : **Charge**")
        else:
            next_question()

elif st.session_state.question_number == 26:
    st.subheader("🧪 Les conditions IAS 38.57 sont-elles toutes remplies ?")
    conditions = st.checkbox("Faisabilité technique") and \
                 st.checkbox("Intention d’achever le projet") and \
                 st.checkbox("Capacité à utiliser ou vendre l'actif") and \
                 st.checkbox("Avantages économiques futurs probables") and \
                 st.checkbox("Ressources disponibles") and \
                 st.checkbox("Dépenses évaluées de façon fiable")
    if st.button("➡️ Suivant", key="b26"):
        if conditions:
            st.success("✅ Conclusion : **Immobilisation incorporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")

# Branche Dépenses liées à un actif
elif st.session_state.question_number == 30:
    st.subheader("🔧 S'agit-il d'une dépense de maintenance ?")
    choix = st.radio("", ["Oui", "Non"], key="q30")
    if st.button("➡️ Suivant", key="b30"):
        if choix == "Oui":
            go_to_question(32)
        else:
            go_to_question(31)

elif st.session_state.question_number == 31:
    st.subheader("🔧 La dépense est-elle directement attribuable à la préparation de l'actif ?")
    choix = st.radio("", ["Oui", "Non"], key="q31")
    if st.button("➡️ Suivant", key="b31"):
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")

elif st.session_state.question_number == 32:
    st.subheader("🔧 La dépense est-elle réalisée avant ou après la mise en service de l’actif ?")
    choix = st.radio("", ["Avant", "Après"], key="q32")
    if st.button("➡️ Suivant", key="b32"):
        if choix == "Après":
            go_to_question(33)
        else:
            go_to_question(34)

elif st.session_state.question_number == 33:
    st.subheader("🔧 La maintenance est-elle évolutive ou corrective ?")
    choix = st.radio("", ["Évolutive", "Corrective"], key="q33")
    if st.button("➡️ Suivant", key="b33"):
        if choix == "Évolutive":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")

elif st.session_state.question_number == 34:
    st.subheader("🔧 Cette dépense est-elle nécessaire pour rendre l’actif opérationnel ?")
    choix = st.radio("", ["Oui", "Non"], key="q34")
    if st.button("➡️ Suivant", key="b34"):
        if choix == "Oui":
            st.success("✅ Conclusion : **Immobilisation corporelle**")
        else:
            st.success("✅ Conclusion : **Charge**")
