import streamlit as st
from datetime import datetime
from scipy.stats import norm
import math
import pandas as pd
from st_aggrid import AgGrid , GridOptionsBuilder
import numpy as np


def Garman_formula(spot, strike, maturity, rd, volatility, option, rf):
    d1 = (1 / (volatility * np.sqrt(maturity))) * (np.log(spot / strike) + (rd - rf + .5 *(volatility ** 2)) * maturity)
    d2 = d1 - volatility * np.sqrt(maturity)
    
    if option == 'call':
        price = spot * np.exp(-rf * maturity) * norm.cdf(d1) - strike * np.exp(-rd * maturity) * norm.cdf(d2)

    elif option == 'put':
        price = strike * np.exp(-rd * maturity) * norm.cdf(-d2) - spot * np.exp(-rf * maturity) * norm.cdf(-d1)

    return price

def Garman_greeks(spot, strike, maturity, rd, volatility, option, rf):

    d1 = (1 / (volatility * np.sqrt(maturity))) * (np.log(spot / strike) + (rd - rf + .5 *(volatility ** 2)) * maturity)

    d2 = d1 - volatility * np.sqrt(maturity)

   

    greeks = dict()

   

    if option == 'call':

        greeks['delta'] = np.exp(-rf * maturity) * norm.cdf(d1, 0, 1)

        greeks['gamma'] = norm.pdf(d1, 0, 1) * np.exp(-rf * maturity) / (spot * volatility * np.sqrt(maturity))

        greeks['rho'] = strike * maturity * np.exp(-rd * maturity) * norm.cdf(d2, 0, 1)

        greeks['vega'] = (spot * norm.pdf(d1, 0, 1) * np.sqrt(maturity) * np.exp(-rf * maturity)/100)

   

    elif option == 'put':

        greeks['delta'] = np.exp(-rf * maturity) * (-norm.cdf(-d1, 0, 1))

        greeks['gamma'] = norm.pdf(d1, 0, 1) * np.exp(-rf * maturity) / (spot * volatility * np.sqrt(maturity))

        greeks['rho'] = -strike * maturity * np.exp(-rd * maturity) * norm.cdf(-d2, 0, 1)

        greeks['vega'] = (spot * norm.pdf(d1, 0, 1) * np.sqrt(maturity) * np.exp(-rf * maturity))/100

       

    return greeks



def option_pricer_page():
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
    st.write("<h3 style='text-align: center;'>Bienvenue dans le pricer d'option FX qui utilise le modèle de Garman-Kohlhagen!</h3>", unsafe_allow_html=True)

    # Create a form context
    with st.form("option_pricer_form"):
        col1 , col2 = st.columns(2)
        with col1 :
        # Add input widgets to the form
            spot = st.number_input("Spot Price:", min_value=0.01, value=100.0,format="%.4f")
            strike = st.number_input("Strike Price:", min_value=0.01, value=100.0,format="%.4f")
            valuation_date = datetime.now().date()  # Obtenir la date de valorisation actuelle
            maturity_date = st.date_input("Date de maturité:")
            option = st.radio('Type d\'option',options=["call","put"])

        with col2 :
            rd = st.number_input("Taux domestique(rd)en %:", min_value=0.0,format="%.4f")
            rf = st.number_input("Taux foreign (rf) en %:", min_value=0.0,format="%.4f")
            volatility = st.number_input("Volatility en %:", min_value=0.0,format="%.4f")
            nominal = st.number_input("Montant:", min_value=0.0,format="%.2f")
        
        

        # Add a submit button to the form
        submitted = st.form_submit_button("Calculer")

    # Calculate
    if submitted:
        rd = rd/100
        rf = rf/100
        volatility = volatility/100
        valuation_datetime = datetime(valuation_date.year, valuation_date.month, valuation_date.day)
        maturity_datetime = datetime(maturity_date.year, maturity_date.month, maturity_date.day)
        maturity = (maturity_datetime - valuation_datetime).days / 360
        price = Garman_formula(spot, strike, maturity, rd, volatility, option, rf)/spot
        greeks = Garman_greeks(spot, strike, maturity, rd, volatility, option, rf)
        prixtot = price * nominal * strike
        
        # Display results in Ag-Grid
        st.write("<h2 style='text-align: center;'>Résultats</h2>", unsafe_allow_html=True)
        df = pd.DataFrame({
                         'Metric': ['Price','Prime en Mad' , 'Delta', 'Gamma', 'Rho', 'Vega'],
                         'Value': [ "{:.4%}".format(price),round(prixtot,4), "{:.4%}".format(round(greeks['delta'],4)), "{:.4%}".format(round(greeks['gamma'],4)), round(greeks['rho'],4), "{:.4%}".format(round(greeks['vega'],4))]
                          })
    
        gb = GridOptionsBuilder.from_dataframe(df)
        grid_options = gb.build()
        AgGrid(df,
               gridOptions=grid_options,
               fit_columns_on_grid_load=True
               )


