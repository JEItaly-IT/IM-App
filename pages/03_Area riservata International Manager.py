import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from PIL import Image
import pandas as pd
import time
import streamlit_authenticator as stauth
import datetime
from math import nan
from login import log_with_mail

# --- Layout comune a tutte le pagine ---
st.set_page_config(page_title='Portale competenze JE Italy', layout = 'wide', initial_sidebar_state = 'auto')
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


if log_with_mail():
# with st.sidebar:
#     st.write('In questa sezione è possibile modificare le informazionin visibili a tutte le altre JE.')

    # --- Collegamento al database Firebase con chiave autenticativa ---
    if not firebase_admin._apps:
        cred = credentials.Certificate('firestore-key.json')
        firebase_admin.initialize_app(cred)
    db = firestore.client()

    # --- Controllo sulle JE inserite nel database in fase di data entry ---
    try:
        lista_je_inserite = []
        doc_ref = db.collection('je_main')
        docs = doc_ref.stream()
        for doc in docs:
            lista_je_inserite.append(doc.to_dict()['nome_completo'])
    except:
        lista_je_inserite = []


    # --- Importing di altri dati utili per il data entry ---
    df = pd.read_excel('ListaUniItaliane.xlsx')
    lista_uni = sorted(df['Università Italiane'].tolist())

    # st.session_state['LOGGED_IN'] = False

    dati_accesso = pd.read_excel('Password_JE.xlsx', index_col=0)
    lista_je = sorted(list(dati_accesso.index.values))


    # if st.session_state['LOGGED_IN'] == False:
    #     st.experimental_memo()

    # --- Login all'interno dell'area riservata agli International Managers delle varie JE italiane ---
    if 'LOGGED_IN' not in st.session_state:
        st.session_state['LOGGED_IN'] = False

    del_login = st.empty()


    if 'utente' in st.session_state:
        if st.session_state['utente'] != 'aaa':
            st.session_state['LOGGED_IN'] = True

    if st.session_state['LOGGED_IN'] == False:
        with del_login.form('inserimento_pw'):
            st.write("Inserire JE e relativa password per accedere all'area riservata")
            junior = st.selectbox('Junior Enterprise', options = lista_je)
            pw = st.text_input('Password', type = 'password')

            
            submitted = st.form_submit_button("Accedi")
            
            if submitted:
                if pw == dati_accesso.loc[junior, 'Password']:
                    st.session_state['LOGGED_IN'] = True
                    st.session_state['utente'] = junior
                    del_login.empty()
                    st.experimental_rerun()
                else:
                    st.warning('⚠️ Password errata')  
                        

    # --- Login effettuato con successo ---
    if st.session_state['LOGGED_IN'] == True :

        if st.button('LOGOUT'):
            st.session_state['LOGGED_IN'] = False
            st.session_state['utente'] = 'aaa'
            st.experimental_rerun()


        st.experimental_memo()

        nome_completo = st.session_state['utente']

        st.header('Area riservata International Manager {}'.format(nome_completo))

        # --- Creazione di due tab per distinguere in due categorie le informazioni di una JE ---
        tab1, tab2 = st.tabs(['Caratteristiche generali JE', 'Caratteristiche nel network'])

        # --- Tab per le caratteristiche generali di una JE ---
        with tab1:
            col1, col2 = st.columns(2)
            
            nome_completo = st.session_state['utente']

            try:
                query = db.collection(u'je_main').document(nome_completo)
                query = query.get()

                def_status = query.to_dict()['status']
                status = col2.text_input('Status', value=def_status, disabled=True)
            except:
                status = col2.selectbox('Status', ['JE', 'JI'])

            try:
                query = db.collection(u'je_main').document(nome_completo)
                query = query.get()
                università_di_riferimento = col1.text_input('Università di riferimento', value=query.to_dict()['università_di_riferimento'], disabled=True)
            except:
                col1.warning('⚠️ Università di riferimento non registrata')
                università_di_riferimento = col1.selectbox('Università di riferimento', lista_uni)

            try:
                query = db.collection(u'je_main').document(nome_completo)
                query = query.get()
                data_di_fondazione = col1.date_input('Data di fondazione',value=datetime.datetime.strptime(query.to_dict()['data_di_fondazione'], '%Y-%m-%d') , disabled=True)
            except:
                col1.warning('⚠️ Data di fondazione non registrata')
                data_di_fondazione = col1.date_input('Data di fondazione', min_value=datetime.datetime.strptime('1980-01-01', '%Y-%m-%d'))

            try:
                query = db.collection(u'je_main').document(nome_completo)
                query = query.get()
                core_business = col2.text_input('Core business', value=query.to_dict()['core_business'])
            except:
                col2.warning('⚠️ Core business non registrato')
                core_business = col2.text_input('Core business')

            try:
                query = db.collection(u'je_main').document(nome_completo)
                query = query.get()
                je_madrina = col1.multiselect('JE madrina/JI affinacata', lista_je, default=query.to_dict()['je_madrina'], 
                help='Per aggiungere una JE madrina o JI affiancate, selezionale dal menù a tendina. Per eliminarle, premi sulla X che si trova\
                    accanto al loro nome.')
            except:
                col1.warning('⚠️ JE madrina o JI affiancata non registrate')
                je_madrina = col1.multiselect('JE madrina/JI affiancata', lista_je, help='Seleziona una o più JE/JI')

            try:
                query = db.collection(u'je_main').document(nome_completo)
                query = query.get()
                associati = col2.number_input('Numero di associati', min_value=0, step=1, value=query.to_dict()['associati'])
            except:
                col2.warning('⚠️ Numero di associati non registrato')
                associati = col2.number_input('Numero di associati', min_value=0, step=1)

            aggiorna = st.button('Modifica caratteristiche della JE')

            if aggiorna and nome_completo != '' and nome_completo not in lista_je_inserite:
                db.collection(u"je_main").document(nome_completo).set({   
                    'nome_completo': nome_completo,
                    'status': status,
                    'data_di_fondazione': str(data_di_fondazione),
                    'università_di_riferimento': università_di_riferimento,
                    'core_business': core_business,
                    'je_madrina': je_madrina,
                    'associati': associati
                    })

                st.success('✔️ Modifica eseguita con successo')
                time.sleep(2)
                st.experimental_rerun()

            elif aggiorna and nome_completo in lista_je_inserite:
                db.collection(u"je_main").document(nome_completo).update({   
                    'nome_completo': nome_completo,
                    'status': status,
                    'core_business': core_business,
                    'je_madrina': je_madrina,
                    'associati': associati
                    })
                st.success('✔️ Modifica eseguita con successo')
                time.sleep(2)
                st.experimental_rerun()


        # --- Tab per le informazioni dinamiche di una JE (competenze, progetti e partnerships) ---
        with tab2:
            
            lista_je = []
            doc_ref = db.collection('je_main')
            docs = doc_ref.stream()
            for doc in docs:
                lista_je.append(doc.to_dict()['nome_completo'])


            try:
                query = db.collection(u'je_main').document(nome_completo)
                query = query.get()
                pitch = st.text_area('Pitch', value=str(query.to_dict()['pitch']), height=150)
            except:
                pitch = st.text_area('⚠️ Pitch mancante. Inizia a scriverne uno!')

            col1, col2 = st.columns(2)


            # --- Sezione progetti ---
            st.subheader('Sezione :blue[progettistica]')
            try:
                query = db.collection(u'je_main').document(nome_completo)
                query = query.get()
                progetti = query.to_dict()['progetti']
                if progetti != []:
                    progetti_del = st.multiselect('Seleziona uno o più progetti da eliminare', progetti)
                    progetti_new = st.text_input('Scrivi il nome del nuovo progetto da aggiungere')

                    if progetti_del != [] and progetti_new == '':
                        progetti = list(set(progetti) - set(progetti_del))
                    elif progetti_del == [] and progetti_new != '' and progetti_new not in progetti:
                        progetti.append(progetti_new)
                    elif progetti_del != [] and progetti_new != '' and progetti_new not in progetti:
                        progetti = list(set(progetti) - set(progetti_del))
                        progetti.append(progetti_new)
                    elif progetti_del != [] and progetti_new != '' and progetti_new in progetti:
                        progetti = list(set(progetti) - set(progetti_del))
                else:
                    progetti = []
                    progetti_new = st.text_input('⚠️ Nessun progetto registrato. Inizia ad aggiungerne uno')
                    if progetti_new != '':
                        progetti.append(progetti_new)
            except:
                progetti = []
                progetti_new = st.text_input('⚠️ Nessun progetto registrato. Inizia ad aggiungerne uno')
                if progetti_new != '':
                    progetti.append(progetti_new)


            # --- Sezione partnerships ---
            st.subheader('Sezione :blue[partnership]')
            try:
                query = db.collection(u'je_main').document(nome_completo)
                query = query.get()
                partners = query.to_dict()['partners']
                if partners != []:
                    partners_del = st.multiselect('Seleziona uno o più partner/s da eliminare', partners)
                    partners_new = st.text_input('Scrivi il nome del nuovo partner da aggiungere')

                    if partners_del != [] and partners_new == '':
                        partners = list(set(partners) - set(partners_del))
                    elif partners_del == [] and partners_new != '' and partners_new not in partners:
                        partners.append(partners_new)
                    elif partners_del != [] and partners_new != '' and partners_new not in partners:
                        partners = list(set(partners) - set(partners_del))
                        partners.append(partners_new)
                    elif partners_del != [] and partners_new != '' and partners_new in partners:
                        partners = list(set(partners) - set(partners_del))
                else:
                    partners = []
                    partners_new = st.text_input('⚠️ Nessuna partnership registrata. Inizia ad aggiungerne una')
                    if partners_new != '':
                        partners.append(partners_new)
            except:
                partners = []
                partners_new = st.text_input('⚠️ Nessuna partnership registrata. Inizia ad aggiungerne una')
                if partners_new != '' and partners_new not in partners:
                    partners.append(partners_new)

            # --- Sezione punti di forza ---
            st.subheader('Sezione :blue[punti di forza]')
            try:
                query = db.collection(u'je_main').document(nome_completo)
                query = query.get()
                punti_di_forza = query.to_dict()['punti_di_forza']
                if punti_di_forza != []:

                    punti_di_forza_del = st.multiselect('Seleziona uno o più punti di forza da eliminare', punti_di_forza)
                    punti_di_forza_new = st.text_input('Scrivi il nome del nuovo punto di forza da aggiungere')

                    if punti_di_forza_del != [] and punti_di_forza_new == '':
                        punti_di_forza = list(set(punti_di_forza) - set(punti_di_forza_del))
                    elif punti_di_forza_del == [] and punti_di_forza_new != '' and punti_di_forza_new not in punti_di_forza:
                        punti_di_forza.append(punti_di_forza_new)
                    elif punti_di_forza_del != [] and punti_di_forza_new != '' and punti_di_forza_new not in punti_di_forza:
                        punti_di_forza = list(set(punti_di_forza) - set(punti_di_forza_del))
                        punti_di_forza.append(punti_di_forza_new)
                    elif punti_di_forza_del != [] and punti_di_forza_new != '' and punti_di_forza_new in punti_di_forza:
                        punti_di_forza = list(set(punti_di_forza) - set(punti_di_forza_del))
                else:
                    punti_di_forza = []
                    punti_di_forza_new = st.text_input('⚠️ Nessuna punto di forza registrato. Inizia ad aggiungerne uno')
                    if punti_di_forza_new != '':
                        punti_di_forza.append(punti_di_forza_new)
            except:
                punti_di_forza = []
                punti_di_forza_new = st.text_input('⚠️ Nessuna punto di forza registrato. Inizia ad aggiungerne uno')
                if punti_di_forza_new != '' and punti_di_forza_new not in punti_di_forza:
                    punti_di_forza.append(punti_di_forza_new)

            # Sezione delle competenze da sviluppare
            my_file = open("Competenze.txt", "r")
            # reading the file
            data = my_file.read()
            # replacing and splitting the text
            lista_competenze = sorted(data.split("\n"))

            # --- Sezione comeptenze da sviluppare ---
            st.subheader('Sezione :blue[competenze da sviluppare]')
            try:
                query = db.collection(u'je_main').document(nome_completo)
                query = query.get()
                competenze_da_sviluppare_0 = query.to_dict()['competenze_da_sviluppare']
                if competenze_da_sviluppare_0 != []:
                    competenze_da_sviluppare = st.multiselect('Gestisci le competenze da sviluppare dalla JE',options=lista_competenze, default=competenze_da_sviluppare_0)
                else:
                    competenze_da_sviluppare = st.multiselect('Gestisci le competenze da sviluppare dalla JE', options=lista_competenze)
            except:
                competenze_da_sviluppare = st.multiselect('Gestisci le competenze da sviluppare dalla JE', options=lista_competenze)

            # --- Sezione delle competenze possedute ---
            st.subheader('Sezione :blue[competenze possedute]')
            try:
                query = db.collection(u'je_main').document(nome_completo)
                query = query.get()
                competenze_possedute_0 = query.to_dict()['competenze_possedute']
                if competenze_possedute_0 != []:
                    competenze_possedute = st.multiselect('Gestisci le competenze possedute dalla JE',options=lista_competenze, default=competenze_possedute_0)  
                else:
                    competenze_possedute = st.multiselect('Gestisci le competenze possedute dalla JE', options=lista_competenze)
            except:
                competenze_possedute = st.multiselect('Gestisci le competenze possedute dalla JE', options=lista_competenze)

            aggiorna = st.button('Modifica')

            if aggiorna and nome_completo in lista_je_inserite:
                db.collection(u"je_main").document(nome_completo).update({
                    'nome_completo': nome_completo,
                    'pitch': str(pitch),
                    'partners': partners,
                    'progetti': progetti,
                    'punti_di_forza': punti_di_forza,
                    'competenze_possedute': competenze_possedute,
                    'competenze_da_sviluppare': competenze_da_sviluppare
                })
                st.success('✔️ Modifica eseguita con successo')
                time.sleep(2)
                st.experimental_rerun()
            elif aggiorna and nome_completo not in lista_je_inserite:
                db.collection(u"je_main").document(nome_completo).set({
                    'nome_completo': nome_completo,
                    'pitch': str(pitch),
                    'partners': partners,
                    'progetti': progetti,
                    'punti_di_forza': punti_di_forza,
                    'competenze_possedute': competenze_possedute,
                    'competenze_da_sviluppare': competenze_da_sviluppare
                })
                st.success('✔️ Modifica eseguita con successo')
                time.sleep(2)
                st.experimental_rerun()

