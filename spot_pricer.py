# spot_pricer.py
import streamlit as st


def spot_pricer_page():
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
    st.write("<h3 style='text-align: center;'>Bienvenue dans le pricer spot!</h3>", unsafe_allow_html=True)
    
    # Demander à l'utilisateur de saisir les données nécessaires
    eur_usd = st.number_input("EUR/USD", min_value=0.0, format= "%.4f")
    liquidite = st.number_input("Liquidité", min_value=-100.0, format= "%.4f")
    marge = st.number_input("marge en pips", min_value=0.0, format= "%.4f")
    transaction_type = st.radio("Type de transaction", ["Achat", "Vente"])
    spot_type = st.radio("Type de spot", ["Clientèle", "Interbancaire"])
     # Calculer les taux de change USD/MAD et EUR/MAD en fonction du type de transaction
        
    alpha = 0.0562307107902725000  # valeur d'alpha
    beta = 0.0397618269539036000  # valeur de beta
    usd_mad = 1 / (alpha * eur_usd + beta) * (1 + liquidite / 1000)
    eur_mad = eur_usd * usd_mad
        
        # Appliquer le facteur de correction en fonction du type de transaction
    if spot_type == "Clientèle":
        if transaction_type == "Achat":
            usd_mad *= 0.999
            eur_mad *= 0.999
            usd_mad += marge/10000
            eur_mad += marge/10000
        else:
            usd_mad *= 1.001
            eur_mad *= 1.001
            usd_mad -= marge/10000
            eur_mad -= marge/10000
        

    if spot_type =="Interbancaire":
        if transaction_type =="Achat":
            usd_mad *= 1
            eur_mad *= 1 
            usd_mad -= marge/10000
            eur_mad -= marge/10000
        else:
            usd_mad *= 1
            eur_mad *= 1 
            usd_mad += marge/10000
            eur_mad += marge/10000

    # Créer deux colonnes pour placer les boutons côte à côte
    col1, col2 = st.columns(2)

# Boutons de calcul
    if col1.button("Calculer EUR/MAD"):
       col1.write(f'<p style="border: 3px solid green; padding:10px; font-size: 20px;"><b>{round(eur_mad, 4)}</b></p>', unsafe_allow_html=True)

    if col2.button("Calculer USD/MAD"):
       col2.write(f'<p style="border: 3px solid blue; padding:10px; font-size: 20px;"><b>{round(usd_mad, 4)}</b></p>', unsafe_allow_html=True) 

