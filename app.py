import streamlit as st
from streamlit_extras.stylable_container import stylable_container

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
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-title">Assistant d\'Analyse Comptable</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">UBCI • Arbre de Décision Automatisé</div>', unsafe_allow_html=True)

if "step" not in st.session_state:
    st.session_state.step = 1

col1, col2 = st.columns([1, 3])
with col2:
    if st.button("🔄 Recommencer"):
        st.session_state.step = 1

# Fonction stylée pour les questions
@stylable_container(key="box", css="border: 1px solid #ccc; border-radius: 16px; padding: 20px; background-color: #f9f9f9;")
def question_box(label, options):
    return st.radio(label, options)

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

# === Questions logiques ===
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

# (Les étapes suivantes restent identiques en logique)
# Tu peux maintenant copier les autres étapes du code précédent ici
# et chaque question passera par question_box pour avoir un look pro
# Les résultats sont présentés avec emojis et couleurs institutionnelles

# Pour aller plus loin, tu peux aussi intégrer le logo UBCI et créer une sidebar d'aide ou de référence réglementaire
# Par exemple :
# st.sidebar.image("https://upload.wikimedia.org/wikipedia/fr/thumb/8/84/UBCI_logo.svg/1200px-UBCI_logo.svg.png", width=150)
# st.sidebar.info("Référence IAS 38, Article 57 pour les conditions de développement interne")
    q35 = st.radio("La dépense est-elle nécessaire pour rendre l’actif opérationnel ?", ["Oui", "Non"])
    if q35 == "Oui":
        show_result("success", "Immobilisation Corporelle")
    else:
        show_result("error", "Charge")
