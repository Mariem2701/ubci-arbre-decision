import streamlit as st

st.set_page_config(
    page_title="Assistant UBCI",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    .big-title {
        font-size: 36px;
        font-weight: bold;
        text-align: center;
        color: #004a99;
        margin-bottom: 10px;
    }
    .subtitle {
        font-size: 18px;
        text-align: center;
        color: #555;
        margin-bottom: 30px;
    }
    .stButton>button {
        font-size: 16px;
        padding: 0.5em 2em;
        background-color: #004a99;
        color: white;
        border-radius: 8px;
    }
    .stRadio>div>label {
        font-size: 16px;
    }
    .question-box {
        border: 1px solid #ccc;
        border-radius: 16px;
        padding: 20px;
        background-color: #f9f9f9;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">Assistant d\'Analyse Comptable</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">UBCI • Arbre de Décision Automatisé</div>', unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 1


def question_box(label, options):
    st.markdown('<div class="question-box">', unsafe_allow_html=True)
    response = st.radio(label, options, key=label)
    st.markdown('</div>', unsafe_allow_html=True)
    return response

def show_next_button(next_step):
    if st.button("Suivant ▶️"):
        st.session_state.step = next_step

def show_result(result_type, message):
    if result_type == "success":
        st.success(f"✅ Conclusion : {message}")
    elif result_type == "error":
        st.error(f"❌ Conclusion : {message}")
    elif result_type == "info":
        st.info(f"ℹ️ Conclusion : {message}")

# === Arbre de Décision Complet ===
if st.session_state.step == 1:
    q1 = question_box("1. La dépense est-elle supérieure à 500 DT ?", ["Oui", "Non"])
    if q1 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(2)

elif st.session_state.step == 2:
    q2 = question_box("2. La dépense concerne-t-elle un bien physique et tangible ?", ["Oui", "Non"])
    if q2 == "Oui":
        show_next_button(3)
    else:
        show_next_button(15)

# === Branche Immobilisations Corporelles ===
elif st.session_state.step == 3:
    q3 = question_box("3. Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?", ["Oui", "Non"])
    if q3 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(4)

elif st.session_state.step == 4:
    q4 = question_box("4. L'entreprise bénéficie-t-elle des avantages économiques futurs du bien ?", ["Oui", "Non"])
    if q4 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(5)

elif st.session_state.step == 5:
    q5 = question_box("5. Le coût du bien peut-il être mesuré de manière fiable ?", ["Oui", "Non"])
    if q5 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(6)

elif st.session_state.step == 6:
    q6 = question_box("6. Les risques et les produits sont-ils transférés à l'entreprise ?", ["Oui", "Non"])
    if q6 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(7)

elif st.session_state.step == 7:
    q7 = question_box("7. La dépense correspond-elle à des frais d’étude ?", ["Oui", "Non"])
    if q7 == "Oui":
        show_next_button(8)
    else:
        show_next_button(9)

elif st.session_state.step == 8:
    q8 = question_box("8. Les frais d’étude sont-ils liés à un actif durable ?", ["Oui", "Non"])
    if q8 == "Oui":
        show_result("success", "Immobilisation corporelle")
    else:
        show_result("error", "Charge")

elif st.session_state.step == 9:
    q9 = question_box("9. S'agit-il d'une nouvelle acquisition ?", ["Oui", "Non"])
    if q9 == "Oui":
        show_result("success", "Immobilisation corporelle")
    else:
        show_next_button(10)

elif st.session_state.step == 10:
    q10 = question_box("10. La valeur vénale de la composante est-elle ≥ 1/4 de la valeur de l'actif ?", ["Oui", "Non"])
    if q10 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(11)

elif st.session_state.step == 11:
    q11 = question_box("11. L'actif est-il identifié dans SAP en tant qu'investissement ?", ["Oui", "Non"])
    if q11 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(12)

elif st.session_state.step == 12:
    q12 = question_box("12. Prolonge-t-il la durée de vie ou améliore-t-il sa performance ?", ["Oui", "Non"])
    if q12 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(13)

elif st.session_state.step == 13:
    q13 = question_box("13. S'agit-il d'une réparation ou réhabilitation majeure ?", ["Réparation", "Réhabilitation majeure"])
    if q13 == "Réhabilitation majeure":
        show_result("success", "Immobilisation corporelle")
    else:
        show_next_button(14)

elif st.session_state.step == 14:
    q14 = question_box("14. La réparation est-elle cyclique (planifiée et répétitive) ?", ["Oui", "Non"])
    if q14 == "Oui":
        show_result("success", "Immobilisation corporelle")
    else:
        show_result("error", "Charge")

# === Branche Immobilisations Incorporelles ===
elif st.session_state.step == 15:
    q15 = question_box("15. L'élément est-il identifiable ?", ["Oui", "Non"])
    if q15 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(16)

elif st.session_state.step == 16:
    q16 = question_box("16. Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?", ["Oui", "Non"])
    if q16 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(17)

elif st.session_state.step == 17:
    q17 = question_box("17. L'entreprise contrôle-t-elle l'élément et en retire-t-elle des avantages économiques futurs probables ?", ["Oui", "Non"])
    if q17 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(18)

elif st.session_state.step == 18:
    q18 = question_box("18. Le coût peut-il être mesuré de manière fiable ?", ["Oui", "Non"])
    if q18 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(19)

elif st.session_state.step == 19:
    q19 = question_box("19. S'agit-il d'une acquisition, d'une création interne ou d'une dépense liée à un actif ?", ["Acquisition", "Création interne", "Dépense liée à un actif"])
    if q19 == "Acquisition":
        show_next_button(20)
    elif q19 == "Création interne":
        show_next_button(25)
    else:
        show_next_button(30)

# Sous-Branche Acquisition
elif st.session_state.step == 20:
    q20 = question_box("L'acquisition concerne-t-elle une licence ?", ["Oui", "Non"])
    if q20 == "Non":
        show_result("success", "Immobilisation incorporelle")
    else:
        show_next_button(21)

elif st.session_state.step == 21:
    q21 = question_box("L'actif est-il hébergé sur une infrastructure contrôlée par l'entreprise ?", ["Oui", "Non"])
    if q21 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(22)

elif st.session_state.step == 22:
    q22 = question_box("L'entreprise dispose-t-elle d'un droit d'usage distinct et exclusif ?", ["Oui", "Non"])
    if q22 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(23)

elif st.session_state.step == 23:
    q23 = question_box("Le droit d’usage est-il permanent ou ≥ 3 ans ?", ["Oui", "Non"])
    if q23 == "Non":
        show_result("error", "Charge")
    else:
        show_next_button(24)

elif st.session_state.step == 24:
    q24 = question_box("Le contrat prévoit-il un abonnement/redevance/paiement récurrent ?", ["Oui", "Non"])
    if q24 == "Oui":
        show_result("error", "Charge")
    else:
        show_result("success", "Immobilisation incorporelle")

# Sous-Branche Création Interne
elif st.session_state.step == 25:
    q25 = question_box("Dépenses de recherche ou de développement ?", ["Recherche", "Développement"])
    if q25 == "Recherche":
        show_result("error", "Charge")
    else:
        show_next_button(26)

elif st.session_state.step == 26:
    q26 = question_box("Les conditions de l’IAS 38.57 sont-elles toutes remplies ?", ["Oui", "Non"])
    if q26 == "Oui":
        show_result("success", "Immobilisation incorporelle")
    else:
        show_result("error", "Charge")

# Sous-Branche Dépense liée à un actif
elif st.session_state.step == 30:
    q30 = question_box("S'agit-il d'une dépense de maintenance ?", ["Oui", "Non"])
    if q30 == "Non":
        show_next_button(31)
    else:
        show_next_button(33)

elif st.session_state.step == 31:
    q31 = question_box("La dépense est-elle directement attribuable à la préparation de l'actif ?", ["Oui", "Non"])
    if q31 == "Oui":
        show_result("success", "Immobilisation corporelle")
    else:
        show_result("error", "Charge")

elif st.session_state.step == 33:
    q33 = question_box("Maintenance avant ou après mise en service ?", ["Avant", "Après"])
    if q33 == "Après":
        show_next_button(34)
    else:
        show_next_button(35)

elif st.session_state.step == 34:
    q34 = question_box("Maintenance évolutive ou corrective ?", ["Évolutive", "Corrective"])
    if q34 == "Évolutive":
        show_result("success", "Immobilisation corporelle")
    else:
        show_result("error", "Charge")

elif st.session_state.step == 35:
    q35 = question_box("Dépense directement nécessaire pour rendre l’actif opérationnel ?", ["Oui", "Non"])
    if q35 == "Oui":
        show_result("success", "Immobilisation corporelle")
    else:
        show_result("error", "Charge")

col1, col2 = st.columns([1, 3])
with col2:
    if st.button("🔄 Recommencer"):
        st.session_state.step = 1
