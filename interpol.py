import streamlit as st

def Calcul_Spot(eur_usd , liquidite , spot_type , transaction_type , devise):
    alpha = 0.0562307107902725000  # valeur d'alpha
    beta = 0.0397618269539036000  # valeur de beta
    usd_mad = 1 / (alpha * eur_usd + beta) * (1 + liquidite / 1000)
    eur_mad = eur_usd * usd_mad

    if spot_type == "Clientèle":
        if transaction_type == "Achat":
            usd_mad *= 0.999
            eur_mad *= 0.999
        else:
            usd_mad *= 1.001
            eur_mad *= 1.001

    if spot_type =="Interbancaire":
        if transaction_type =="Achat":
            usd_mad *= 1
            eur_mad *= 1 
        else:
            usd_mad *= 1
            eur_mad *= 1

    return usd_mad if devise == 'usd' else eur_mad

def Calcul_liquidite(eur_usd, usd_mad, spot_type, transaction_type, devise):
    alpha = 0.0562307107902725000
    beta = 0.0397618269539036000
    liquidite = (usd_mad * (alpha * eur_usd + beta) - 1) * 1000
    if spot_type == "Clientèle":
        if transaction_type == "Achat":
            usd_mad /= 0.999
        else:
            usd_mad /= 1.001
    elif spot_type == "Interbancaire":
        if transaction_type == "Achat":
            usd_mad /= 1
        else:
            usd_mad /= 1
    eur_mad = eur_usd * usd_mad
    return liquidite if devise == 'usd' else liquidite / eur_mad

def spot_pricer_page2():
    st.markdown(
    """
    <style>
    .title {
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    # Afficher le titre centré
    st.markdown("<h1 class='title'>PRICER SPOT</h1>", unsafe_allow_html=True)
    st.write("<h3 style='text-align: center;'>Bienvenue dans le pricer spot!</h3>",unsafe_allow_html=True)
    
    spot_type = st.radio("Spot Type", ("Clientèle", "Interbancaire"))
    transaction_type = st.radio("Transaction Type", ("Achat", "Vente"))
    eur_usd = st.number_input("EUR/USD", value=1.0,format="%.4f")

    col1 , col2 = st.columns(2)

    eur_mad = 0.0  # Initialize eur_mad with a default value
    usd_mad = 0.0  # Initialize usd_mad with a default value
    liquidite = 0.0  # Initialize liquidite with a default value

    with col1:
        eur_mad_input = st.empty()
        usd_mad_input = st.empty()
        liquidite_input = st.empty()
        liquidite = float(liquidite_input.text_input("Liquidite", value=str(liquidite)))
        eur_mad = float(eur_mad_input.text_input("EUR/MAD", value=str(eur_mad), key="eur_mad"))
        usd_mad = float(usd_mad_input.text_input("USD/MAD", value=str(usd_mad), key="usd_mad"))
        

    with col2:
        st.write("")
        st.write("")

        if st.button("Calculer EUR/MAD"):
            eur_mad = round(Calcul_Spot(eur_usd, liquidite, spot_type, transaction_type, "eur"),4)
            eur_mad_input.text_input("EUR/MAD", value=str(eur_mad), key="eur_mad1")
        
        st.write("")
        st.write("")

        if st.button("Calculer USD/MAD"):
            usd_mad = round(Calcul_Spot(eur_usd, liquidite, spot_type, transaction_type, "usd"),4)
            usd_mad_input.text_input("USD/MAD", value=str(usd_mad), key="usd_mad1")
        
        st.write("")
        st.write("")
        if st.button("Calculer Liquidité"):
            liquidite = round(Calcul_liquidite(eur_usd, usd_mad, spot_type, transaction_type, "usd"),4)
            liquidite_input.text_input("Liquidite", value=str(liquidite))
        

        




    



