import streamlit as st
import pandas as pd
import pydeck as pdk
import base64
from PIL import Image
from login import log_with_mail


# st.markdown(
#          f"""
#          <style>
#          .stApp {{
#              background-image: url("https://www.incimages.com/uploaded_files/image/1920x1080/getty_681735120_359777.jpg");
#              background-attachment: fixed;
#              background-size: cover
#          }}
#          </style>
#          """,
#          unsafe_allow_html=True
#      )

logo_JE = Image.open('JE_logo.png')
#  logo_jesap = Image.open('Jesap.png')
st.set_page_config(page_title='Portale competenze JE Italy', layout = 'wide', page_icon = logo_JE, initial_sidebar_state = 'auto')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.header('Portale competenze Junior Enterprise italiane')

col1, col2, col3 = st.columns(3)

col2.image(logo_JE, width=200)



st.markdown('Benvenuti nella **Dashboard Interattiva delle Junior Enterprise Italiane**. Questa piattaforma vi offre un accesso\
        completo e dettagliato a tutte le informazioni sulle **Junior Enterprise** italiane, inclusi data di fondazione, numero di associati,\
            punti di forza, competenze e molto altro. Con questa dashboard, è possibile visualizzare facilmente le informazioni riguardo le\
                JE e confrontare i loro dati per avere una panoramica completa sul network italiano.')

st.markdown('Inoltre, la piattaforma offre anche la possibilità di aggiornare le informazioni sulle JE, riservata\
            agli **International Manager**. Ciò significa che è possibile mantenere i dati sempre aggiornati e precisi,\
                garantendo dunque la continua affidabilità dei dati qui presentati.')

#st.markdown('<p style="padding: 1px 0;">Powered by <b>JESAP Consulting</b></p>', unsafe_allow_html=True)
#col4, col5, col6 = st.columns(3)

#col6.image(logo_jesap, caption='Powered by JESAP Consulting', width=150)
#col6.write('Powered by JESAP Consulting')

def get_css():
    with open("stile.css") as f:
        css = f.read()
    return css

# Aggiunge lo stile del CSS 
def set_css():
    css = get_css()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

st.markdown("""
	<head>
		<link rel="stylesheet" type="text/css" href="stile.css">
	</head>
	<body>
		<div class="mioDiv">
			<img src="https://jesap.it/wp-content/uploads/2021/05/Civetta-definitivo-gradiente-_aggiornato.png" width="100" height="100">
			<p>Powered by Jesap Consulting</p>
		</div>
	</body>
""", unsafe_allow_html=True)

set_css()



# col1, col2 = st.columns(2, gap = 'medium')


# with col1:
#     st.image('icons\\JEB.png', width = 170 )
#     st.markdown(f"""
#     **Nome completo**: {'Jeb Consulting'} \n
#     **Data di fondazione**: {'25.11.2021'} \n
#     **Status**: {'JI'} \n
#     **Università di riferimento**: {'Università degli studi di Bergamo'} \n
#     **Core Business**: {'Consulenza IT'} """)
    
    
    
    

# with col2:
#     st.markdown(f"""Pitch: \n
#     Progetto in collaborazione: \n
#     Punti di forza: \n
#     Competenze/conoscenze da sviluppare: \n
#     Partners: """)