import streamlit as st
from datetime import datetime
from scipy.stats import norm
import plotly.graph_objects as go
import numpy as np


def option_Hes_pricer_page():
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

    
    st.markdown("<h1 class='title'>FX OPTIONS PRICER</h1>", unsafe_allow_html=True)
    st.write("<h3 style='text-align: center;'>Bienvenue dans le pricer d'option FX qui utilise le modèle de Heston!</h3>", unsafe_allow_html=True)

    # Ask the user to input the necessary data
    S = st.number_input("Prix spot", min_value=0.0, format="%.4f")
    K = st.number_input("Strike", min_value=0.0, format="%.4f")
    valuation_date = datetime.now().date()  # Get the current valuation date
    maturity_date = st.date_input("Date de Maturité")
    r = st.number_input("Taux d'interet local", min_value=0.0, format="%.4f")
    q = st.number_input("Taux d'interet étranger", min_value=0.0, format="%.4f")
    sigma = st.number_input("Volatilité", min_value=0.0, format="%.4f")
    kappa = st.number_input("Vitesse de réversion", min_value=0.0, format="%.4f")
    theta = st.number_input("volatilité à long terme", min_value=0.0, format="%.4f")
    option_type = st.radio("type d'option", ["Call", "Put"])
    rho = 0
    # Ajouter un bouton calculer
    if st.button("Calculate"):
        valuation_datetime = datetime(valuation_date.year, valuation_date.month, valuation_date.day)
        maturity_datetime = datetime(maturity_date.year, maturity_date.month, maturity_date.day)
        T = (maturity_datetime - valuation_datetime).days / 365

        # parametres de simulation
        N = 10  # nombre de pas 
        M = 1000  # Number de simulations

        # initializer les arrays pour les prix et variance
        S_sim = np.zeros((N+1, M))
        v_sim = np.zeros((N+1, M))

        # valeurs initiales
        S_sim[0] = S
        v_sim[0] = sigma ** 2

        # generer les variables aléatoires
        Z1 = np.random.standard_normal((N, M))
        Z2 = rho * Z1 + np.sqrt(1 - rho ** 2) * np.random.standard_normal((N, M))

        # simulation
        dt = T / N
        for i in range(1, N+1):
            S_sim[i] = S_sim[i-1] * np.exp((r - q - 0.5 * v_sim[i-1]) * dt + np.sqrt(v_sim[i-1] * dt) * Z1[i-1])
            v_sim[i] = v_sim[i-1] + kappa * (theta - v_sim[i-1]) * dt + sigma * np.sqrt(v_sim[i-1] * dt) * Z2[i-1]
            v_sim[i] = np.maximum(v_sim[i], 0)  # Ensure variance is non-negative

        # calculer les prix d'option
        if option_type == "Call":
            option_prices = np.maximum(S_sim[-1] - K, 0)
        else:
            option_prices = np.maximum(K - S_sim[-1], 0)

        # Discount option prices
        discount_factor = np.exp(-r * T)
        option_prices *= discount_factor

        # Calculate option price as the average of all scenarios
        option_price = np.mean(option_prices)

        # arrondir le resultat 
        option_price = round(option_price, 4)

        # Display the result
        st.subheader("Résultat")
        st.markdown(f'<font color="green" size="+6">Le prix est : {option_price}</font>', unsafe_allow_html=True)

        # Création du graphique
        fig = go.Figure()

        # Adding the Monte Carlo simulation results to the plot
        for i in range(M):
           fig.add_trace(go.Scatter(x=np.arange(N+1), y=S_sim[:, i], mode='lines', name=f'Simulation {i+1}'))

        fig.update_layout(
            title="Simulation de Monte Carlo (Modèle de Heston)",
            xaxis_title="Pas de temps",
            yaxis_title="Prix (S)",
            showlegend=True,
            legend_title="Simulations",
            width=800,
            height=500,
            plot_bgcolor='grey'
        )

        # Afficher le graphique dans Streamlit
        st.plotly_chart(fig)