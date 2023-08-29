import streamlit as st
from datetime import datetime
from scipy.stats import norm
import math

def option_pricer_page2():
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
    st.markdown("<h1 class='title'>FX OPTIONS PRICER</h1>", unsafe_allow_html=True)
    st.write("<h3 style='text-align: center;'>Bienvenue dans le pricer d'option FX qui utilise le modèle de Black-Scholes!</h3>", unsafe_allow_html=True)

    # Demander à l'utilisateur de saisir les données nécessaires
    S = st.number_input("Prix spot", min_value=0.0, format="%.4f")
    K = st.number_input("Strike", min_value=0.0, format="%.4f")
    valuation_date = datetime.now().date()  # Obtenir la date de valorisation actuelle
    maturity_date = st.date_input("Date de maturité")
    r = st.number_input("Taux d'interet local en %", min_value=0.0, format="%.4f")
    q = st.number_input("Taux d'interet étranger %", min_value=0.0, format="%.4f")
    sigma = st.number_input("Volatilité", min_value=0.0, format="%.4f")
    option_type = st.radio("type d'option", ["Call", "Put"])

    # Ajouter un bouton "Calculer"
    if st.button("Calculer"):
        valuation_datetime = datetime(valuation_date.year, valuation_date.month, valuation_date.day)
        maturity_datetime = datetime(maturity_date.year, maturity_date.month, maturity_date.day)
        T = (maturity_datetime - valuation_datetime).days / 365
        r = r/100
        q = q/100
        # Calculer les paramètres d1 et d2 du modèle de Black-Scholes
        d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)

        # Calculer le prix de l'option en fonction du type d'option
        if option_type == "Call":
            option_price = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
        else:
            option_price = K * math.exp(-r * T) * norm.cdf(-d2) - S * math.exp(-q * T) * norm.cdf(-d1)

        # Calculer les sensibilités de l'option (Grecques)
        delta = norm.cdf(d1) if option_type == "Call" else norm.cdf(d1) - 1
        gamma = norm.pdf(d1) / (S * sigma * math.sqrt(T))
        vega = S * norm.pdf(d1) * math.sqrt(T)
        theta = -(S * sigma * norm.pdf(d1)) / (2 * math.sqrt(T)) - r * K * math.exp(-r * T) * norm.cdf(d2) if option_type == "Call" else -(S * sigma * norm.pdf(d1)) / (2 * math.sqrt(T)) + r * K * math.exp(-r * T) * norm.cdf(-d2)

        # Arrondir le résultat à 4 chiffres après la virgule
        option_price = round(option_price, 4)
        delta = round(delta, 4)
        gamma = round(gamma, 4)
        vega = round(vega, 4)
        theta = round(theta, 4)

        # Afficher le résultat
        st.subheader("Résultat")
        st.markdown(f'<font color="green" size="+6">Le prix de l\'option est : {option_price}</font>', unsafe_allow_html=True)

        st.subheader("Sensibilités (Grecques)")
        st.write(f"Delta : {delta}")
        st.write(f"Gamma : {gamma}")
        st.write(f"Vega : {vega}")
        st.write(f"Theta : {theta}")
