# main.py
import streamlit as st
from spot_pricer import spot_pricer_page
from option_pricer import option_pricer_page
from streamlit_option_menu import option_menu
from option_Hes_pricer import option_Hes_pricer_page
from Pricer_A_Terme import forward_rate_pricer_page
from Bs_pricer import option_pricer_page2
from interpol import spot_pricer_page2



   
    
    
st.sidebar.image("traderlogo_prev_ui_prev_ui.png" , use_column_width=True)

    
    #barre laterale pour selectionner les pages 
selected = option_menu(
        menu_title= None , 
        options= ["Pricer spot","Spot2","FX Options Pricer(GK)","FX options pricer(Heston)","Change à termes","BS Pricer"],
        orientation= "horizontal",

    )

if selected == "Pricer spot":
    spot_pricer_page()

if selected == "FX Options Pricer(GK)":
    option_pricer_page()

if selected == "FX options pricer(Heston)" :
    option_Hes_pricer_page()

if selected == "Change à termes":
    forward_rate_pricer_page()
    
if selected == "BS Pricer":
    option_pricer_page2()
if selected == "Spot2":
    spot_pricer_page2()

