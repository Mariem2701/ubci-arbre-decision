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

def reset():
    st.session_state.question_number = 1
    st.session_state.history = []

# Bouton pour recommencer depuis le début
st.sidebar.button("🔄 Réinitialiser", on_click=reset)
if st.session_state.question_number == 1:
    st.subheader("1️⃣ La dépense est-elle supérieure à 500 DT ?")

    choix = st.radio("Réponse :", ["Oui", "Non"], key="q1")

    if st.button("➡️ Suivant"):
        st.session_state.history.append(("Q1", choix))

        if choix == "Oui":
            next_question()  # aller à la prochaine question
        else:
            st.success("✅ Conclusion : Cette dépense est comptabilisée en **Charge**.")
# Question 2
elif st.session_state.question_number == 2:
    st.subheader("2️⃣ La dépense concerne-t-elle un bien physique et tangible ?")
    choix = st.radio("Réponse :", ["Oui", "Non"], key="q2")
    if st.button("➡️ Suivant", key="b2"):
        st.session_state.history.append(("Q2", choix))
        if choix == "Oui":
            next_question()
        else:
            go_to_question(15)  # Vers les incorporelles

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
