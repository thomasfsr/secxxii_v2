import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

def auth_page():
    with open('auth_config.yml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )

    authenticator.login()

    if st.session_state.get("authentication_status"):
        #authenticator.logout(button_name= ':red[logout]')
        return True
    elif st.session_state.get("authentication_status") is False:
        st.error('Usuário/Senha inválido')
        return False
    elif st.session_state.get("authentication_status") is None:
        st.warning('Por Favor, utilize seu usuário e senha!')
        return False
