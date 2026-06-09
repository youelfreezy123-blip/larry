import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Calculateur Douane", layout="centered")

st.title("️ Calculette Douanière : CAF & MDT")
st.write("Calculez facilement votre Valeur CAF ou le Montant Total des Droits (MDT).")

# Remplacement de l'input de choix par une boîte de sélection Streamlit
choix = st.selectbox(
    "Que voulez-vous calculer ?",
    ["-- Choisir une option --", "1. Valeur CAF", "2. Montant des Droits de Douane (MDT)"]
)

# --- OPTION 1 : CALCUL CAF ---
if choix == "1. Valeur CAF":
    st.header("⚙️ Calcul de la Valeur CAF")

    # Formulaire pour regrouper les entrées de manière propre
    with st.form("form_caf"):
        col1, col2 = st.columns(2)
        with col1:
            fob_unitaire = st.number_input("FOB Unitaire", min_value=0, value=0, step=1)
            nombre_de_colie = st.number_input("Nombre de colis", min_value=0, value=0, step=1)
            fret = st.number_input("Valeur Fret", min_value=0, value=0, step=1)
        with col2:
            assmaritime = st.number_input("Assurance Maritime", min_value=0, value=0, step=1)
            asslocal = st.number_input("Assurance Locale", min_value=0, value=0, step=1)

        soumettre_caf = st.form_submit_button("Calculer la CAF")

    if soumettre_caf:
        if nombre_de_colie > 0:
            # Calculs
            fob_total = fob_unitaire * nombre_de_colie
            asslocalr1 = asslocal + 1000
            asslacalr2 = asslocalr1 * 5 / 100
            asslocalr3 = asslocalr1 + asslacalr2
            ass_total = assmaritime + asslocalr3
            caf = fob_total + ass_total + fret

            # Affichage des résultats
            st.success("### Résultats du calcul")
            st.metric(label="Valeur CAF (Valeur en Douane)", value=f"{caf:,.2f} FCFA")

            # Tableau récapitulatif détaillé avec Pandas
            details = {
                "Indicateur": ["FOB Total", "Assurance Locale Finale", "Assurance Totale", "Valeur CAF"],
                "Montant": [fob_total, asslocalr3, ass_total, caf]
            }
            df_details = pd.DataFrame(details)
            st.dataframe(df_details, use_container_width=True, hide_index=True)
        else:
            st.error("Le nombre de colis doit être supérieur à 0.")

# --- OPTION 2 : CALCUL MDT ---
elif choix == "2. Montant des Droits de Douane (MDT)":
    st.header(" Calculateurs des Taxes (MDT)")

    with st.form("form_mdt"):
        valeur_en_douane = st.number_input("Entrez la Valeur en Douane (CAF)", min_value=0.0, value=0.0, step=100.0)
        soumettre_mdt = st.form_submit_button("Calculer les Droits de Douane")

    if soumettre_mdt:
        # Calculs des taxes fiscales locales (Sénégal/UEMOA)
        redevance_statistique = valeur_en_douane * 1 / 100
        prelevement_communautaire_solidarite = valeur_en_douane * 0.8 / 100
        prelevement_communautaire_cdao = valeur_en_douane * 0.5 / 100
        cosec = valeur_en_douane * 0.4 / 100
        promad = valeur_en_douane * 2 / 100
        tva = valeur_en_douane * 18 / 100
        bic = valeur_en_douane * 3 / 100

        MDT = (redevance_statistique + prelevement_communautaire_solidarite +
               prelevement_communautaire_cdao + cosec + promad + tva + bic)

        # Affichage du résultat principal
        st.success("### Montant Total à Payer")
        st.metric(label="Montant Total des Droits (MDT)", value=f"{MDT:,.2f} FCFA")

        # Génération du rapport de taxes avec Pandas
        taxes_data = {
            "Type de Taxe / Redevance": [
                "Redevance Statistique (RS)",
                "Prélèvement Communautaire de Solidarité (PCS)",
                "Prélèvement Communautaire CEDEAO (PCC)",
                "COSEC",
                "PROMAD",
                "TVA",
                "Acompte BIC"
            ],
            "Taux": ["1.0%", "0.8%", "0.5%", "0.4%", "2.0%", "18.0%", "3.0%"],
            "Montant (FCFA)": [
                redevance_statistique,
                prelevement_communautaire_solidarite,
                prelevement_communautaire_cdao,
                cosec,
                promad,
                tva,
                bic
            ]
        }
        df_taxes = pd.DataFrame(taxes_data)

        st.write("**Détail des taxes prélevées :**")
        st.dataframe(df_taxes, use_container_width=True, hide_index=True)

# --- AUCUN CHOIX ---
else:
    st.info("Veuillez sélectionner une option dans le menu déroulant ci-dessus pour démarrer.")
