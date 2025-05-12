import streamlit as st

st.set_page_config(page_title="Assistant UBCI", page_icon=":bank:", layout="centered")

# Initialiser l'état
if "step" not in st.session_state:
    st.session_state.step = 1

if st.button("🔄 Recommencer"):
    st.session_state.step = 1

# Fonction d'affichage dynamique
def show_next_button(next_step):
    if st.button("Suivant ▶️"):
        st.session_state.step = next_step

def show_result(result_type, message):
    if result_type == "success":
        st.success(f"Conclusion : {message}")
    elif result_type == "error":
        st.error(f"Conclusion : {message}")
    elif result_type == "info":
        st.info(f"Conclusion : {message}")

# Déroulement par étapes
if st.session_state.step == 1:
    q1 = st.radio("1. La dépense est-elle supérieure à 500 DT ?", ["Oui", "Non"])
    if q1 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(2)

elif st.session_state.step == 2:
    q2 = st.radio("2. La dépense concerne-t-elle un bien physique et tangible ?", ["Oui", "Non"])
    if q2 == "Oui":
        show_next_button(3)
    else:
        show_next_button(15)

# Partie Immobilisation Corporelle
elif st.session_state.step == 3:
    q3 = st.radio("3. Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?", ["Oui", "Non"])
    if q3 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(4)

# ... Les étapes 4 à 14 seraient ici ... (pour ne pas surcharger ce bloc)

# Partie Immobilisation Incorporelle
elif st.session_state.step == 15:
    q15 = st.radio("15. L’élément est-il identifiable ?", ["Oui", "Non"])
    if q15 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(16)

elif st.session_state.step == 16:
    q16 = st.radio("16. Est-il destiné à être utilisé pour plus d'un exercice ?", ["Oui", "Non"])
    if q16 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(17)

elif st.session_state.step == 17:
    q17 = st.radio("17. L'entreprise contrôle-t-elle l'élément et en tire-t-elle des avantages économiques futurs ?", ["Oui", "Non"])
    if q17 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(18)

elif st.session_state.step == 18:
    q18 = st.radio("18. Le coût peut-il être mesuré de manière fiable ?", ["Oui", "Non"])
    if q18 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(19)

elif st.session_state.step == 19:
    q19 = st.radio("19. Nature de la dépense ?", ["Acquisition", "Création Interne", "Dépense liée à un actif"])
    if q19 == "Acquisition":
        show_next_button(20)
    elif q19 == "Création Interne":
        show_next_button(25)
    else:
        show_next_button(30)

# Sous-branche Acquisition
elif st.session_state.step == 20:
    q20 = st.radio("L'acquisition concerne-t-elle une licence ?", ["Oui", "Non"])
    if q20 == "Non":
        show_result("success", "Immobilisation Incorporelle")
    else:
        show_next_button(21)

elif st.session_state.step == 21:
    q21 = st.radio("L'actif est-il hébergé sur une infrastructure contrôlée par l’entreprise ?", ["Oui", "Non"])
    if q21 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(22)

elif st.session_state.step == 22:
    q22 = st.radio("L’entreprise dispose-t-elle d’un droit d’usage distinct et exclusif de l’actif ?", ["Oui", "Non"])
    if q22 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(23)

elif st.session_state.step == 23:
    q23 = st.radio("Le droit d’usage est-il permanent ou pour ≥ 3 ans ?", ["Oui", "Non"])
    if q23 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(24)

elif st.session_state.step == 24:
    q24 = st.radio("Le contrat prévoit-il un abonnement/redevance ?", ["Oui", "Non"])
    if q24 == "Oui":
        show_result("error", "Charge")
    else:
        show_result("success", "Immobilisation Incorporelle")

# Sous-branche Création Interne
elif st.session_state.step == 25:
    q25 = st.radio("Nature de la création ?", ["Recherche", "Développement"])
    if q25 == "Recherche":
        show_result("error", "Charge")
    else:
        show_next_button(26)

elif st.session_state.step == 26:
    q26 = st.radio("Toutes les conditions IAS 38.57 sont-elles remplies ?", ["Oui", "Non"])
    if q26 == "Oui":
        show_result("success", "Immobilisation Incorporelle")
    else:
        show_result("error", "Charge")

# Sous-branche Dépense liée à un actif
elif st.session_state.step == 30:
    q30 = st.radio("S'agit-il d'une dépense de maintenance ?", ["Oui", "Non"])
    if q30 == "Non":
        show_next_button(31)
    else:
        show_next_button(33)

elif st.session_state.step == 31:
    q31 = st.radio("La dépense est-elle directement attribuable à la préparation de l'actif ?", ["Oui", "Non"])
    if q31 == "Oui":
        show_result("success", "Immobilisation Corporelle")
    else:
        show_result("error", "Charge")

elif st.session_state.step == 33:
    q33 = st.radio("Maintenance avant ou après mise en service ?", ["Avant", "Après"])
    if q33 == "Avant":
        show_next_button(35)
    else:
        show_next_button(34)

elif st.session_state.step == 34:
    q34 = st.radio("Type de maintenance après mise en service ?", ["Évolutive", "Corrective"])
    if q34 == "Évolutive":
        show_result("success", "Immobilisation Corporelle")
    else:
        show_result("error", "Charge")

elif st.session_state.step == 35:
    q35 = st.radio("La dépense est-elle nécessaire pour rendre l’actif opérationnel ?", ["Oui", "Non"])
    if q35 == "Oui":
        show_result("success", "Immobilisation Corporelle")
    else:
        show_result("error", "Charge")
