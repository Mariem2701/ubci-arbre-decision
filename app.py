
import streamlit as st

st.set_page_config(page_title="Assistant UBCI", page_icon=":bank:", layout="centered")

# Initialiser l'état
if "step" not in st.session_state:
    st.session_state.step = 1

if st.button("🔄 Recommencer"):
    st.session_state.step = 1

# Étape 1
if st.session_state.step == 1:
    q1 = st.radio("1. La dépense est-elle supérieure à 500 DT ?", ["Oui", "Non"])
    if q1 == "Non":
        st.error("Conclusion : Charge")
    else:
        if st.button("Suivant"):
            st.session_state.step = 2

# Étape 2
elif st.session_state.step == 2:
    q2 = st.radio("2. La dépense concerne-t-elle un bien physique et tangible ?", ["Oui", "Non"])
    if q2 == "Oui":
        if st.button("Continuer vers Immobilisation Corporelle"):
            st.session_state.step = 3
    else:
        if st.button("Continuer vers Immobilisation Incorporelle"):
            st.session_state.step = 15

# --- IMMOBILISATION CORPORELLE ---
elif st.session_state.step == 3:
    q3 = st.radio("3. Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?", ["Oui", "Non"])
    if q3 == "Non":
        st.error("Conclusion : Charge")
    else:
        if st.button("Suivant"):
            st.session_state.step = 4

elif st.session_state.step == 4:
    q4 = st.radio("4. L'entreprise bénéficie-t-elle des avantages économiques futurs du bien ?", ["Oui", "Non"])
    if q4 == "Non":
        st.error("Conclusion : Charge")
    else:
        if st.button("Suivant"):
            st.session_state.step = 5

elif st.session_state.step == 5:
    q5 = st.radio("5. Le coût du bien peut-il être mesuré de manière fiable ?", ["Oui", "Non"])
    if q5 == "Non":
        st.error("Conclusion : Charge")
    else:
        if st.button("Suivant"):
            st.session_state.step = 6

elif st.session_state.step == 6:
    q6 = st.radio("6. Les risques et les produits sont-ils transférés à l'entreprise ?", ["Oui", "Non"])
    if q6 == "Non":
        st.error("Conclusion : Charge")
    else:
        if st.button("Suivant"):
            st.session_state.step = 7

elif st.session_state.step == 7:
    q7 = st.radio("7. La dépense correspond-elle à des frais d’étude ?", ["Oui", "Non"])
    if q7 == "Oui":
        if st.button("Suivant"):
            st.session_state.step = 8
    else:
        if st.button("Suivant"):
            st.session_state.step = 9

elif st.session_state.step == 8:
    q8 = st.radio("8. Les frais d’étude sont-ils directement liés à un actif durable ?", ["Oui", "Non"])
    if q8 == "Oui":
        st.success("Conclusion : Immobilisation Corporelle")
    else:
        st.error("Conclusion : Charge")

elif st.session_state.step == 9:
    q9 = st.radio("9. S'agit-il d'une nouvelle acquisition ?", ["Oui", "Non"])
    if q9 == "Oui":
        st.success("Conclusion : Immobilisation Corporelle")
    else:
        if st.button("Continuer vers Grosse Réparation"):
            st.session_state.step = 10

# --- SOUS-BRANCHE GROSSES RÉPARATIONS ---
elif st.session_state.step == 10:
    q10 = st.radio("10. La valeur vénale de la composante >= 1/4 de la valeur de l'actif ?", ["Oui", "Non"])
    if q10 == "Non":
        st.error("Conclusion : Charge")
    else:
        if st.button("Suivant"):
            st.session_state.step = 11

elif st.session_state.step == 11:
    q11 = st.radio("11. L'actif initial est-il identifié dans SAP en tant qu'investissement ?", ["Oui", "Non"])
    if q11 == "Non":
        st.error("Conclusion : Charge")
    else:
        if st.button("Suivant"):
            st.session_state.step = 12

elif st.session_state.step == 12:
    q12 = st.radio("12. Prolonge-t-il la durée de vie ou augmente sa performance ?", ["Oui", "Non"])
    if q12 == "Non":
        st.error("Conclusion : Charge")
    else:
        if st.button("Suivant"):
            st.session_state.step = 13

elif st.session_state.step == 13:
    q13 = st.radio("13. S'agit-il d’une réparation ou d'une réhabilitation majeure ?", ["Réparation", "Réhabilitation majeure"])
    if q13 == "Réhabilitation majeure":
        st.success("Conclusion : Immobilisation Corporelle")
    else:
        if st.button("Suivant"):
            st.session_state.step = 14

elif st.session_state.step == 14:
    q14 = st.radio("14. La réparation présente-t-elle un caractère cyclique ?", ["Oui", "Non"])
    if q14 == "Oui":
        st.success("Conclusion : Immobilisation Corporelle")
    else:
        st.error("Conclusion : Charge")

# --- IMMOBILISATION INCORPORELLE ---
elif st.session_state.step == 15:
    q15 = st.radio("15. L’élément est-il identifiable ?", ["Oui", "Non"])
    if q15 == "Non":
        st.error("Conclusion : Charge")
    else:
        if st.button("Suivant"):
            st.session_state.step = 16

elif st.session_state.step == 16:
    q16 = st.radio("16. Est-il destiné à être utilisé plus d'un exercice ?", ["Oui", "Non"])
    if q16 == "Non":
        st.error("Conclusion : Charge")
    else:
        if st.button("Suivant"):
            st.session_state.step = 17

elif st.session_state.step == 17:
    q17 = st.radio("17. L'entreprise contrôle-t-elle l'élément et en tire des avantages économiques ?", ["Oui", "Non"])
    if q17 == "Non":
        st.error("Conclusion : Charge")
    else:
        if st.button("Suivant"):
            st.session_state.step = 18

elif st.session_state.step == 18:
    q18 = st.radio("18. Le coût peut-il être mesuré de manière fiable ?", ["Oui", "Non"])
    if q18 == "Non":
        st.error("Conclusion : Charge")
    else:
        if st.button("Suivant"):
            st.session_state.step = 19

elif st.session_state.step == 19:
    q19 = st.radio("19. S'agit-il d'une acquisition, création interne ou dépense liée à un actif ?", ["Acquisition", "Création Interne", "Dépense liée à un actif"])
    if q19 == "Acquisition":
        st.success("Conclusion (à développer) : Immobilisation Incorporelle par Acquisition")
    elif q19 == "Création Interne":
        st.success("Conclusion (à développer) : Immobilisation Incorporelle en interne")
    else:
        st.success("Conclusion (à développer) : Dépense liée à un actif")

