import streamlit as st
from streamlit_option_menu import option_menu
import comandas, cadastro_clientes, servicos, registros, calendar_service, check
import auth

st.set_page_config(
    page_title='Século XXII',
    layout='wide', page_icon=':shoe:'
)

if not auth.auth_page():
    st.stop() 

def init_state():
    if 'page' not in st.session_state:
        st.session_state.page = 'Comanda'

init_state()

def render_page():
    if st.session_state.page == 'Novo Cliente':
        cadastro_clientes.app()
    elif st.session_state.page == 'Comanda':
        comandas.app()
    elif st.session_state.page == 'Serviços':
        servicos.app()
    elif st.session_state.page == 'Registro':
        registros.app()
    elif st.session_state.page == 'Calendário':
        calendar_service.app()
    elif st.session_state.page == 'Check':
        check.app()


selected_page = option_menu(
    menu_title='Século XXII',
    options=['Comanda','Serviços','Calendário','Check','Registro','Novo Cliente'],
    icons=['cart','table','calendar3','check2-square','cash-coin','person-circle'],
    menu_icon='stack',
    default_index=0,
    orientation='horizontal',
    styles={
        "container": {"padding": "4px", "background-color": "#f0f2f2"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "18px", 
                     "text-align": "center", 
                     "margin":"0px", 
                     "--hover-color": "#e1e9f0",
                     "font-family": "Arial, Helvetica, sans-serif"
                     },
        "nav-link-selected": {"background-color": "#3e474f",
                              "font-size": "16px"}
    }
)
st.session_state.page = selected_page

reload = st.button(':green[**RECARREGAR PÁGINA** ] :repeat:', help='Caso o menu não esteja aparecendo', use_container_width=False)
if reload:
    st.rerun()

render_page()