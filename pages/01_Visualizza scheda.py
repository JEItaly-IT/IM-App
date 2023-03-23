import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from PIL import Image
import pandas as pd
import datetime
from login import log_with_mail

# --- Collegamento al database di Firebase tramite chiave autenticativa ---
if not firebase_admin._apps:
    cred = credentials.Certificate('firestore-key.json')
    firebase_admin.initialize_app(cred)
db = firestore.client()

# --- Layout comune a tutte le pagine ---
st.set_page_config(page_title='Portale competenze JE Italy', layout = 'wide', initial_sidebar_state = 'auto')
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- Login iniziale appartenenza JE ---
if log_with_mail():

    # --- Creazione Visualizzazione scheda ---
    junior = pd.read_excel('locations_and_logos.xlsx', sheet_name='logos')

    col1, col2 = st.columns(2)

    with col1:
        aree = list(set(junior['zona']))
        aree.sort()
        area = st.selectbox('Area Geografica', aree)

    with col2:
        je_area = list(set(junior[junior['zona'] == area]['tags']))
        je_area.sort()
        chosen = st.selectbox('Junior Enterprise', je_area)


    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')
    st.write(' ')





    logo = junior[junior['tags'] == chosen]['icon_data'].values[0]



    try:
        query = db.collection(u'je_main').document(chosen)
        query = query.get()
        status = query.to_dict()['status']
    except:
        status = 'Status non registrato'

    try:
        query = db.collection(u'je_main').document(chosen)
        query = query.get()
        università_di_riferimento = query.to_dict()['università_di_riferimento']
    except:
        università_di_riferimento = 'Università di riferimento non registrata'
        

    try:
        query = db.collection(u'je_main').document(chosen)
        query = query.get()
        data_di_fondazione = datetime.datetime.strptime(query.to_dict()['data_di_fondazione'], '%Y-%m-%d')
    except:
        data_di_fondazione = 'Data di fondazione non registrata'



    try:
        query = db.collection(u'je_main').document(chosen)
        query = query.get()
        core_business = query.to_dict()['core_business']
    except:
        core_business = 'Core business non registrato'
        
            
            
    try:
        query = db.collection(u'je_main').document(chosen)
        query = query.get()
        je_madrina = query.to_dict()['je_madrina'] 
        if je_madrina == []:
            je_madrina = 'JE madrina o JI affiancata non registrate.'
    except:
        je_madrina = 'JE madrina o JI affiancata non registrate.'
        

    try:
        query = db.collection(u'je_main').document(chosen)
        query = query.get()
        associati = query.to_dict()['associati']
    except:
        associati = 'Numero di associati non registrato.'
        

    try:
        query = db.collection(u'je_main').document(chosen)
        query = query.get()
        pitch = str(query.to_dict()['pitch'])
    except:
        pitch = 'Pitch mancante.'

    try:
        query = db.collection(u'je_main').document(chosen)
        query = query.get()
        progetti = list(query.to_dict()['progetti'])

        if progetti == []:
            progetti = 'Nessun progetto registrato.'
    except:
        progetti = 'Nessun progetto registrato.'



    if je_madrina !=  'JE madrina o JI affiancata non registrate.' and je_madrina != []:
        madrina_associati = ''

        for i in je_madrina[:-1]:
            madrina_associati = madrina_associati + i + ', '

        madrina_associati = madrina_associati + je_madrina[-1] + '.'

        je_madrina = madrina_associati



    try:
        query = db.collection(u'je_main').document(chosen)
        query = query.get()
        partners = query.to_dict()['partners']
        if partners == []:
            partners = 'Nessuna partnership registrata.'
    except:
        partners = 'Nessuna partnership registrata.'





    try:
        query = db.collection(u'je_main').document(chosen)
        query = query.get()
        punti_di_forza = list(query.to_dict()['punti_di_forza'])
            
            
        if punti_di_forza == []:
            punti_di_forza = 'Nessuna punto di forza inserito.'

    except:
        punti_di_forza = 'Nessuna punto di forza inserito.'



    with st.expander('Vedi Scheda'):

        col1, col2 = st.columns(2)

        with col1:
            st.image(logo, width = 170 )
            st.markdown(f"""
            **:blue[Nome completo]**: {chosen} \n
            **:blue[Data di fondazione]**: {data_di_fondazione} \n
            **:blue[Status]**: {status} \n
            **:blue[Università di riferimento]**: {università_di_riferimento} \n
            **:blue[Core Business]**: {core_business} \n
            **:blue[JE madrina/JI affiancata]**: {je_madrina}  \n
            **:blue[Numero di associati]**: {associati} """)
            
            
            
            

        with col2:
            st.markdown(f'**:blue[Pitch]**: {pitch}') 

            st.write(' ')

            if punti_di_forza == 'Nessuna punto di forza inserito.':
                st.markdown(f'**:blue[Punti di forza]**: {punti_di_forza}')
            else:
                st.markdown('**:blue[Punti di forza]**: ')
                for p in punti_di_forza:
                    st.markdown(f'* {p}')

        


        




    st.write('')
    st.write('')


    # --- Expander per Partner e Progetti ---
    with st.expander('Partner e progetti'):
        col5, col6 = st.columns(2)


        with col5:
            if partners == 'Nessuna partnership registrata.':
                st.markdown(f'**:blue[Partnerships]**: {partners}')
            else:
                st.markdown('**:blue[Partnerships]**: ')
                for partner in partners:
                    st.markdown(f'* {partner}')





        with col6:
            if progetti != 'Nessun progetto registrato.':
                
                st.markdown('**:blue[Progetti in collaborazione]:** \n')
                
                for progetto in progetti:
                    st.markdown(f'''* {progetto} \n''')

            else:
                st.markdown(f'**:blue[Progetti in collaborazione]:** {progetti}')   








    st.write(' ')
    st.write(' ')



    # --- Expander per le competenze presenti o da sviluppare in JE ---
    with st.expander('Competenze'):
        col3, col4 = st.columns(2)




        query = db.collection(u'je_main').document(chosen)
        query = query.get()
        competenze_possedute = query.to_dict()['competenze_possedute']
        competenze_da_sviluppare = query.to_dict()['competenze_da_sviluppare']





        with col3:
            st.markdown('### :green[Competenze possedute]')
            st.write('')
            st.write('')
            for comp in competenze_possedute:
                st.markdown(f'* {comp} ✅')
            if competenze_possedute == []:
                st.markdown('Nessuna competenza posseduta registrata.')

        with col4:
            st.markdown('### :orange[Competenze da sviluppare]')
            st.write('')
            st.write('')
            for comp in competenze_da_sviluppare:
                st.markdown(f'* {comp} ⏳')
            if competenze_da_sviluppare == []:
                st.markdown('Nessuna competenza da sviluppare registrata.')
