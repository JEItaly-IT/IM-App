import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from PIL import Image
import pydeck as pdk
import pandas as pd
from login import log_with_mail

# --- Collegamento al database Firebase con chiave autenticativa ---
if not firebase_admin._apps:
    cred = credentials.Certificate('firestore-key.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

# --- Layout comune a tutte le pagine ---
logo_JE = Image.open('JE_logo.png')
st.set_page_config(page_title='Portale competenze JE Italy', layout = 'wide', page_icon = logo_JE, initial_sidebar_state = 'auto')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- Login appartenenza a una JE con email associativa ---
if log_with_mail():



    data = pd.read_excel('locations_and_logos.xlsx', sheet_name='logos')

    scatter = pd.read_excel('locations_and_logos.xlsx', sheet_name='scatter')


    tratte = pd.DataFrame(columns = ['start', 'end'], index = data.index)


    # Sezione delle competenze da sviluppare
    my_file = open("Competenze.txt", "r")
    # reading the file
    nomi = my_file.read()
    # replacing and splitting the text
    lista_competenze = sorted(nomi.split("\n"))


    for i in data.index:
        parte = [data.loc[i, 'lon'], data.loc[i, 'lat']]
        arriva = [scatter.loc[i, 'lon'], scatter.loc[i, 'lat']]


        tratte.at[i, 'start'] = parte
        tratte.at[i, 'end'] = arriva


    # file = open('icone.txt', 'r')

    file = open('base64.txt', 'r')

    letto = file.read()

    icone = letto.split()

    data['icon_data'] = icone

    for i in data.index:
        data.at[i, 'icon_data'] = {
                            "url": data.at[i, 'icon_data'],
                            "width": 242,
                            "height": 242,
                            "anchorY": 242,
                        }



    dati_accesso = pd.read_excel('Password_JE.xlsx', index_col=0)
    lista_je = list(dati_accesso.index.values)


    col1, col2 = st.columns([3,1])

    competenze_richieste = col1.multiselect('Competenze desiderate', options = lista_competenze)
    col2.write(' ')
    col2.write(' ')
    anche_da_sviluppare = col2.checkbox('Visualizza anche se in fase di sviluppo')

    # --- Creazione delle mappe in funzione delle competenze selezionate ---
    if competenze_richieste == []:
        
        line_layer = pdk.Layer(
            "LineLayer",
            data = tratte,
            get_source_position="start",
            get_target_position="end",
            get_width=1,
            # highlight_color=[0, 0, 0],
            # picking_radius=10,
            # auto_highlight=True,
            # pickable=True,
        )

        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data = tratte,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position="end",
            get_radius= 5,
            get_fill_color=[0, 0, 0],
            get_line_color=[0, 0, 0],
        )

        icon_layer = pdk.Layer(
            type="IconLayer",
            data=data.iloc[:, :-1],
            get_icon="icon_data",
            get_size=3,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True,
        )

        view_state = pdk.ViewState(12.7442, 42.5, 4.3)


        r = pdk.Deck(map_style = "mapbox://styles/mapbox/light-v9", 
                    layers=[line_layer, icon_layer, scatter_layer], 
                    initial_view_state=view_state, tooltip={"text": "{tags}"})     

        st.pydeck_chart(r)



    else:

        je_da_mostrare = []

        for ind, je in enumerate(lista_je):
            try:
                query = db.collection(u'je_main').document(je)
                query = query.get()
                competenze_possedute = query.to_dict()['competenze_possedute']
                competenze_da_sviluppare = query.to_dict()['competenze_da_sviluppare']
                competenze_totali = list(set(competenze_possedute + competenze_da_sviluppare))


                if anche_da_sviluppare == False:
                    check =  all(item in competenze_possedute for item in competenze_richieste)
                else:
                    check =  all(item in competenze_totali for item in competenze_richieste)
                    

                if check == True:
                    je_da_mostrare.append(ind)
            except:
                continue

        line_layer = pdk.Layer(
            "LineLayer",
            data = tratte.iloc[je_da_mostrare, :],
            get_source_position="start",
            get_target_position="end",
            get_width=1,
            # highlight_color=[0, 0, 0],
            # picking_radius=10,
            # auto_highlight=True,
            # pickable=True,
        )

        scatter_layer = pdk.Layer(
            "ScatterplotLayer",
            data = tratte.iloc[je_da_mostrare, :],
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position="end",
            get_radius= 5,
            get_fill_color=[0, 0, 0],
            get_line_color=[0, 0, 0],
        )

        icon_layer = pdk.Layer(
            type="IconLayer",
            data=data.iloc[je_da_mostrare, :-1],
            get_icon="icon_data",
            get_size=3,
            size_scale=15,
            get_position=["lon", "lat"],
            pickable=True,
        )

        view_state = pdk.ViewState(12.7442, 42.5, 4.3)


        r = pdk.Deck(map_style = "mapbox://styles/mapbox/light-v9", 
                    layers=[line_layer, icon_layer, scatter_layer], 
                    initial_view_state=view_state, tooltip={"text": "{tags}"})     

        st.pydeck_chart(r)

        st.write(' ')
        st.write(' ')

    # st.table(data.iloc[je_da_mostrare, :-1])

   