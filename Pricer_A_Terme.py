import streamlit as st
from datetime import datetime
import numpy as np
import pandas as pd

data = pd.read_excel("DataBidAsk.xlsx")


# Fonction d'interpolation
def interpolate_and_convert_percentage(data, values_to_interpolate, columns_to_interpolate):
    values_to_interpolate = np.array(values_to_interpolate)  # Convertir en tableau unidimensionnel
    result_data = {'NbDays': values_to_interpolate}
    for column in columns_to_interpolate:
        interpolated_values = np.interp(values_to_interpolate, data['NbDays'], data[column])
        result_data[column] = interpolated_values
    
    return pd.DataFrame(result_data)



def forward_rate_pricer_page():
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
    st.markdown("<h1 class='title'>PRICER CHANGE A TERMES</h1>", unsafe_allow_html=True)
    st.write("<h3 style='text-align: center;'>Bienvenue dans le pricer de taux de change à termes!</h3>", unsafe_allow_html=True)


    # Demander à l'utilisateur de saisir les données nécessaires
    S = st.number_input("Prix Spot", min_value=0.0, format="%.4f")
    devise = st.selectbox("Devise", ["USD", "EUR"])
    valuation_date = datetime.now().date()  # Obtenir la date de valorisation actuelle
    maturity_date = st.date_input("Date de maturité")
    sens = st.radio("Sens de transaction",["Achat","Vente"])
    valuation_datetime = datetime(valuation_date.year, valuation_date.month, valuation_date.day)
    maturity_datetime = datetime(maturity_date.year, maturity_date.month, maturity_date.day)
    T = (maturity_datetime - valuation_datetime).days / 365

    def forward(data, NbDays, devise, cours_spot, sens):
      taux=interpolate_and_convert_percentage(data,[T],['BID_USD', 'ASK_USD', 'BID_EUR','ASK_EUR','BID_MAD','ASK_MAD'])

      if sens == "Achat":
        if devise == 'USD':  
          taux_forward = cours_spot * (1 + (taux['BID_MAD'] * NbDays / 360)) / (1 + (taux['ASK_USD'] * NbDays / 360))
        else:
          taux_forward = cours_spot * (1 + (taux['BID_MAD'] * NbDays / 360)) / (1 + (taux['ASK_EUR'] * NbDays / 360))
        
      else:
        if devise == 'USD':  
          taux_forward = cours_spot * (1 + (taux['ASK_MAD'] * NbDays / 360)) / (1 + (taux['BID_USD'] * NbDays / 360))
        else:
          taux_forward = cours_spot * (1 + (taux['ASK_MAD'] * NbDays / 360)) / (1 + (taux['BID_EUR'] * NbDays / 360))
        
      return taux_forward
    
    # Ajouter un bouton "Calculer"
    if st.button("Calculer"):
        valuation_datetime = datetime(valuation_date.year, valuation_date.month, valuation_date.day)
        maturity_datetime = datetime(maturity_date.year, maturity_date.month, maturity_date.day)
        NbDays = (maturity_datetime - valuation_datetime).days
        cours_spot = S
        taux=interpolate_and_convert_percentage(data,[T],['BID_USD', 'ASK_USD', 'BID_EUR','ASK_EUR','BID_MAD','ASK_MAD'])
        df = pd.DataFrame(taux)
        
        # Calculer le taux de change à terme 
        forward_rate = forward(data, NbDays, devise, cours_spot, sens)

        # Extract the scalar value and format the forward_rate to display up to 4 decimal places
        formatted_forward_rate = "{:.4f}".format(forward_rate.item())
        col1 , col2 = st.columns(2)
        # Afficher le résultat
        with col1:
          st.subheader("Résultat:")
          st.markdown(f'<div style="border: 3px solid black; padding: 10px; display: inline-block;"><p style="color:green; font-size:24px;">Le taux de change à terme est : <span style="color:red;">{formatted_forward_rate}</span></p></div>', unsafe_allow_html=True)
        with col2:   
          st.subheader("Les taux sont:")
          st.dataframe(df)