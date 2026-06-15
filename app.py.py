import streamlit as st
import pandas as pd

# Configuration de la page
st.set_page_config(page_title="Calculateur Douanier", page_icon="🛃", layout="centered")

st.title("🛃 Calculateur de Droits de Douane & Assurance")
st.write("Remplissez les champs ci-dessous pour générer la liquidation douanière.")

# --- ÉTAPE 1 : CHOIX DU NOMBRE D'ARTICLES ---
choix = st.radio("Combien d'articles voulez-vous calculer ?", options=[1, 2], horizontal=True)

# Initialisation des variables pour éviter les erreurs de calcul global
fob_total = 0.0
cfr = 0.0
fret = 0.0
fob_unitaire_1 = 0.0
fob_unitaire_2 = 0.0
fob_unitaire_1_total = 0.0
fob_unitaire_2_total = 0.0
poid_u1 = 1.0
poid_u2 = 1.0
poid_total = 1.0

# --- ÉTAPE 2 : ENTRÉE DES VALEURS FOB & FRET ---
st.subheader("📦 Valeurs FOB & Fret")

if choix == 1:
    col1, col2 = st.columns(2)
    with col1:
        fob_unitaire = st.number_input("Entrez la FOB unitaire :", min_value=0, value=0, step=1)
    with col2:
        nombre_de_colie = st.number_input("Entrez le nombre de colis :", min_value=0, value=0, step=1)

    fob_total = float(fob_unitaire * nombre_de_colie)
    st.metric(label="Valeur FOB Totale", value=f"{fob_total:,.2f}")

    fret = st.number_input("Entrez la valeur du Fret :", min_value=0, value=0, step=1)
    cfr = fob_total + fret
    st.metric(label="Valeur CFR", value=f"{cfr:,.2f}")

elif choix == 2:
    st.markdown("**Article 1**")
    col1, col2, col3 = st.columns(3)
    with col1:
        fob_unitaire_1 = st.number_input("FOB unitaire Art 1 :", min_value=0, value=0, step=1)
    with col2:
        nombre_de_colie_1 = st.number_input("Nombre colis Art 1 :", min_value=0, value=0, step=1)
    with col3:
        poid_u1 = st.number_input("Poids brut Art 1 :", min_value=0.0, value=0.0, step=0.1)

    st.markdown("**Article 2**")
    col4, col5, col6 = st.columns(3)
    with col4:
        fob_unitaire_2 = st.number_input("FOB unitaire Art 2 :", min_value=0, value=0, step=1)
    with col5:
        nombre_de_colie_2 = st.number_input("Nombre colis Art 2 :", min_value=0, value=0, step=1)
    with col6:
        poid_u2 = st.number_input("Poids brut Art 2 :", min_value=0.0, value=0.0, step=0.1)

    poid_total = poid_u1 + poid_u2 if (poid_u1 + poid_u2) > 0 else 1.0
    fob_unitaire_1_total = float(fob_unitaire_1 * nombre_de_colie_1)
    fob_unitaire_2_total = float(fob_unitaire_2 * nombre_de_colie_2)
    fob_total = fob_unitaire_1_total + fob_unitaire_2_total

    st.info(
        f"📋 **Poids Total :** {poid_total} | **FOB Art 1 :** {fob_unitaire_1_total:,.2f} | **FOB Art 2 :** {fob_unitaire_2_total:,.2f} | **FOB Total :** {fob_total:,.2f}")

    fret = st.number_input("Entrez la valeur du Fret global :", min_value=0, value=0, step=1)
    cfr = fob_total + fret
    st.metric(label="Valeur CFR Totale", value=f"{cfr:,.2f}")

# --- ÉTAPE 3 : ASSURANCE TRANSPORT ---
st.subheader("🛡️ Assurance Transport")
mode_assurance = st.selectbox(
    "Choisissez votre mode de calcul de l'assurance transport :",
    options=[
        "1. J'ai la valeur de l'assurance (Maritime / Locale)",
        "2. Calculer avec CFR + Majoration %",
        "3. Calculer avec le CIF"
    ]
)

ass_total = 0.0

if "1." in mode_assurance:
    col1, col2 = st.columns(2)
    with col1:
        assmaritime = st.number_input("Assurance Maritime :", min_value=0, value=0, step=1)
    with col2:
        asslocal = st.number_input("Assurance Locale :", min_value=0, value=0, step=1)

    asslocalr3 = (asslocal + 1000) * 1.05
    ass_total = float(assmaritime + asslocalr3)

elif "2." in mode_assurance:
    col1, col2 = st.columns(2)
    with col1:
        p_simple = st.number_input("Pourcentage simple assurance (ex: 4) :", min_value=0.0, value=0.0)
    with col2:
        p_majoret = st.number_input("Pourcentage majoré assurance (ex: 10) :", min_value=0.0, value=0.0)
    asslocal = st.number_input("Assurance Locale :", min_value=0, value=0, step=1)

    ass_a_retenir = (1 + (p_majoret / 100)) * (p_simple / 100)
    assurance_cfr_maj = cfr * ass_a_retenir
    asslocalr3 = (asslocal + 1000) * 1.05
    ass_total = float(assurance_cfr_maj + asslocalr3)

elif "3." in mode_assurance:
    col1, col2 = st.columns(2)
    with col1:
        p_simple = st.number_input("Pourcentage simple assurance (ex: 4) :", min_value=0.0, value=0.0)
    with col2:
        p_majoret = st.number_input("Pourcentage majoré assurance (ex: 10) :", min_value=0.0, value=0.0)
    asslocal = st.number_input("Assurance Locale :", min_value=0, value=0, step=1)

    ass_a_retenir = (1 + (p_majoret / 100)) * (p_simple / 100)
    pourcentage_cif_maj = cfr / (1 - ass_a_retenir) if (1 - ass_a_retenir) > 0 else cfr
    assurance_cif_exact = pourcentage_cif_maj - cfr
    asslocalr3 = (asslocal + 1000) * 1.05
    ass_total = float(assurance_cif_exact + asslocalr3)

st.metric(label="Assurance Totale Retenue", value=f"{ass_total:,.2f}")

# --- ÉTAPE 4 : TAXES ET DROITS DE DOUANE ---
st.subheader("🏛️ Paramètres de Liquidation Douanière")

# Dictionnaires des taux pour la liste déroulante
dict_categories = {"Catégorie 0 (0%)": 0.0, "Catégorie 1 (5%)": 0.05, "Catégorie 2 (10%)": 0.10,
                   "Catégorie 3 (20%)": 0.20, "Catégorie 4 (35%)": 0.35}

# Options fiscales globales ou par article
if choix == 1:
    cat_douane = st.selectbox("Catégorie de droit de douane :", options=list(dict_categories.keys()))
    taux_dd = dict_categories[cat_douane]

    ajoute_droit_assise = st.checkbox("Ajouter la taxe Droit d'Assise ?")
    taux_assise = 0.0
    if ajoute_droit_assise:
        taux_assise = st.number_input("Entrez le taux du droit d'assise (%) :", min_value=0.0, value=5.0) / 100

    promad_ajoute = st.checkbox("Ajouter la taxe PROMAD (2%) ?")

elif choix == 2:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Configurations Article 1**")
        cat_douane_1 = st.selectbox("Catégorie douane Article 1 :", options=list(dict_categories.keys()), key="cat1")
        taux_dd_1 = dict_categories[cat_douane_1]

        ajoute_droit_assise_1 = st.checkbox("Ajouter la taxe Droit d'Assise (Art 1) ?", key="assise_art1")
        taux_assise_1 = 0.0
        if ajoute_droit_assise_1:
            taux_assise_1 = st.number_input("Taux du droit d'assise Art 1 (%) :", min_value=0.0, value=5.0,
                                            key="taux_assise_art1") / 100

        promad_ajoute_1 = st.checkbox("Ajouter la taxe PROMAD (2%) (Art 1) ?", key="promad_art1")

    with col2:
        st.markdown("**Configurations Article 2**")
        cat_douane_2 = st.selectbox("Catégorie douane Article 2 :", options=list(dict_categories.keys()), key="cat2")
        taux_dd_2 = dict_categories[cat_douane_2]

        ajoute_droit_assise_2 = st.checkbox("Ajouter la taxe Droit d'Assise (Art 2) ?", key="assise_art2")
        taux_assise_2 = 0.0
        if ajoute_droit_assise_2:
            taux_assise_2 = st.number_input("Taux du droit d'assise Art 2 (%) :", min_value=0.0, value=5.0,
                                            key="taux_assise_art2") / 100

        promad_ajoute_2 = st.checkbox("Ajouter la taxe PROMAD (2%) (Art 2) ?", key="promad_art2")


# --- FONCTION DE CALCUL D'UN ARTICLE (Pandas & Dataframe) ---
def calculer_liquidation(nom_art, caf_art, taux_dd, taux_assise, inclure_promad):
    dd = caf_art * taux_dd
    rs = caf_art * 0.01
    pcs = caf_art * 0.008
    pc_cdao = caf_art * 0.005
    cosec = caf_art * 0.004

    da = (caf_art + dd + rs) * taux_assise if taux_assise > 0 else 0.0
    promad = caf_art * 0.02 if inclure_promad else 0.0

    # Assiette TVA et BIC inclut le droit d'assise si existant
    assiette_tva_bic = caf_art + dd + rs + da
    tva = assiette_tva_bic * 0.18
    bic = assiette_tva_bic * 0.03

    mdt = dd + rs + pcs + pc_cdao + da + cosec + promad + tva + bic

    donnees = {
        "Taxe / Élément": ["Valeur en Douane (CAF)", "Droit de Douane", "Redevance Statistique", "PCS",
                           "Prélèvement CDAO", "Droit d'Assise", "COSEC", "PROMAD", "TVA", "BIC",
                           "TOTAL À PAYER (MDT)"],
        "Montant": [caf_art, dd, rs, pcs, pc_cdao, da, cosec, promad, tva, bic, mdt]
    }
    return pd.DataFrame(donnees), mdt


# --- ÉTAPE 5 : CALCUL ET AFFICHAGE DES RÉSULTATS ---
st.markdown("---")
if st.button("🔥 CALCULER LA LIQUIDATION DOUANIÈRE", type="primary"):

    if fob_total <= 0:
        st.error("Veuillez entrer des valeurs FOB valides avant de calculer.")
    else:
        if choix == 1:
            caf_total = fob_total + ass_total + fret
            df_resultat, mdt_total = calculer_liquidation("Article Unique", caf_total, taux_dd, taux_assise,
                                                          promad_ajoute)

            st.success(f"### 🧾 Montant Total à Payer en Douane : {mdt_total:,.0f} F CFA")
            st.dataframe(df_resultat.style.format({"Montant": "{:,.2f}"}), use_container_width=True)

        elif choix == 2:
            # Répartition proportionnelle de l'assurance et du fret
            ass_art1 = ass_total * fob_unitaire_1_total / fob_total if fob_total > 0 else 0.0
            ass_art2 = ass_total * fob_unitaire_2_total / fob_total if fob_total > 0 else 0.0

            fret_art1 = fret * poid_u1 / poid_total
            fret_art2 = fret * poid_u2 / poid_total

            caf_art1 = fob_unitaire_1_total + ass_art1 + fret_art1
            caf_art2 = fob_unitaire_2_total + ass_art2 + fret_art2

            # --- CORRECTION ICI ---
            # Injection des variables spécifiques (1 et 2) de chaque article dans la fonction de calcul
            df_art1, mdt_1 = calculer_liquidation("Article 1", caf_art1, taux_dd_1, taux_assise_1, promad_ajoute_1)
            df_art2, mdt_2 = calculer_liquidation("Article 2", caf_art2, taux_dd_2, taux_assise_2, promad_ajoute_2)

            mdt_global = mdt_1 + mdt_2

            st.success(f"### 🧾 MONTANT TOTAL GLOBAL À PAYER : {mdt_global:,.0f} F CFA")

            tab1, tab2 = st.tabs(["📦 Premier Article", "📦 Deuxième Article"])
            with tab1:
                st.metric(label="Droit de douane Article 1", value=f"{mdt_1:,.2f}")
                st.dataframe(df_art1.style.format({"Montant": "{:,.2f}"}), use_container_width=True)
            with tab2:
                st.metric(label="Droit de douane Article 2", value=f"{mdt_2:,.2f}")
                st.dataframe(df_art2.style.format({"Montant": "{:,.2f}"}), use_container_width=True)