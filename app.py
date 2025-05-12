import streamlit as st

def main():
    st.title("Assistant Comptable UBCI : Arbre de Décision")

    # Question 1
    q1 = st.radio("1. La dépense est-elle supérieure à 500 DT ?", ("Oui", "Non"))
    if q1 == "Non":
        st.error("Conclusion : Charge")
        return

    # Question 2
    q2 = st.radio("2. La dépense concerne-t-elle un bien physique et tangible ?", ("Oui", "Non"))
    
    if q2 == "Oui":
        immobilisation_corporelle()
    else:
        immobilisation_incorporelle()

def immobilisation_corporelle():
    st.subheader("Branche des Immobilisations Corporelles")

    q3 = st.radio("3. Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?", ("Oui", "Non"))
    if q3 == "Non":
        st.error("Conclusion : Charge")
        return

    q4 = st.radio("4. L'entreprise bénéficie-t-elle des avantages économiques futurs du bien ?", ("Oui", "Non"))
    if q4 == "Non":
        st.error("Conclusion : Charge")
        return

    q5 = st.radio("5. Le coût du bien peut-il être mesuré de manière fiable ?", ("Oui", "Non"))
    if q5 == "Non":
        st.error("Conclusion : Charge")
        return

    q6 = st.radio("6. Les risques et les produits sont-ils transférés à l'entreprise ?", ("Oui", "Non"))
    if q6 == "Non":
        st.error("Conclusion : Charge")
        return

    q7 = st.radio("7. La dépense correspond-elle à des frais d’étude ?", ("Oui", "Non"))
    if q7 == "Oui":
        q8 = st.radio("8. Les frais d’étude sont-ils directement liés à un actif durable ?", ("Oui", "Non"))
        if q8 == "Oui":
            st.success("Conclusion : Immobilisation Corporelle")
        else:
            st.error("Conclusion : Charge")
    else:
        q9 = st.radio("9. S'agit-il d'une nouvelle acquisition ?", ("Oui", "Non"))
        if q9 == "Oui":
            st.success("Conclusion : Immobilisation Corporelle")
        else:
            st.info("On passe à la sous-branche des grosses réparations (à développer dans la suite)")

def immobilisation_incorporelle():
    st.subheader("Branche des Immobilisations Incorporelles")

    q15 = st.radio("15. L’élément est-il identifiable ?", ("Oui", "Non"))
    if q15 == "Non":
        st.error("Conclusion : Charge")
        return

    q16 = st.radio("16. Est-il destiné à être utilisé pour plus d'un exercice (> 1 an) ?", ("Oui", "Non"))
    if q16 == "Non":
        st.error("Conclusion : Charge")
        return

    q17 = st.radio("17. L'entreprise contrôle-t-elle l'élément et en retire-t-elle des avantages économiques futurs ?", ("Oui", "Non"))
    if q17 == "Non":
        st.error("Conclusion : Charge")
        return

    q18 = st.radio("18. Le coût peut-il être mesuré de manière fiable ?", ("Oui", "Non"))
    if q18 == "Non":
        st.error("Conclusion : Charge")
        return

    q19 = st.radio("19. S'agit-il d'une acquisition, création interne ou dépense liée à un actif ?", ("Acquisition", "Création Interne", "Dépense liée à un actif"))
    
    if q19 == "Acquisition":
        st.info("On passe à la branche Acquisition (à développer)")
    elif q19 == "Création Interne":
        st.info("On passe à la branche Création Interne (à développer)")
    else:
        st.info("On passe à la branche Dépense liée à un actif (à développer)")

if __name__ == "__main__":
    main()
