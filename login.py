import streamlit as st
from validate_email import validate_email


def log_with_mail():
    if 'logmail' not in st.session_state:
        st.session_state['logmail'] = False


    if 'utent' in st.session_state:
        if st.session_state['utent'] != 'aaa':
            st.session_state['logmail'] = True

    if st.session_state['logmail'] == False:
            st.sidebar.title("Effettua l'accesso")
            mail= st.sidebar.text_input("Inserisci il tuo indirizzo e-mail relativo alla tua JE:")
            passwordd= st.sidebar.text_input("Inserisci password:",  type="password")
            st.session_state['vm'] = None
            vm=validate_email(mail) 
            
            button = st.sidebar.button("Accedi")
            
            if button:
                if vm is True and passwordd== mail.split("@")[1].split(".")[0] + "competenze23":
                    st.session_state['vm'] = True
                    st.session_state['logmail'] = True
                    st.session_state['utent'] = mail
                    st.experimental_rerun()
                else:
                    st.warning('⚠️mail o password errate')  
                        
    return st.session_state['vm']

