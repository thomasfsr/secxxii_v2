from streamlit_calendar import calendar
import streamlit as st
from connectdb_sqlite import Sqlite_db
import pandas as pd
from datetime import datetime


def create_events(servicos:pd.DataFrame):
    events = []
    for _, servico in servicos.iterrows():
        event_id = servico['comanda_id']
        nome = servico['nome']
        tel = servico['tel']
        desc = servico['servico']
        status_name = servico['status_name']
        valor_restante = servico['valor_restante']
        data_entrega = servico['data_entrega']
        data_entrega = pd.to_datetime(servico['data_entrega'], format='%d-%m-%Y')
        # formatted_data_entrega = data_entrega.strftime('%Y-%m-%dT%H:%M:%S')
        formatted_data_entrega = data_entrega.strftime('%Y-%m-%d')
        if status_name == 'A FAZER':
            color = 'red'
        elif status_name == 'PRONTO':
            color = 'blue'
        else:
            color = 'green'

        events.append({
            'allDay':True,
            'id': event_id,
            'title': f'{str(event_id)}-{nome}',
            'nome': nome,
            'tel' : tel,
            'desc': desc,
            'status': status_name,
            'valor_restante': valor_restante,
            'date': formatted_data_entrega,
            'backgroundColor': color,
            'borderColor':color
        })
    return events


def app():
    motor = Sqlite_db()
    motor.connect()
    query = '''
    select c.comanda_id,
            c.cliente_id,
            cl.nome,
            cl.tel,
            c.servico,
            c.preco_total,
            c.sinal,
            c.valor_restante,
            c.data_entrada,
            c.data_entrega,
            c.data_retirada,
            c.status_name
    from comandas c
    join clientes cl on cl.cliente_id = c.cliente_id;
    '''
    # carregar dados necessários
    servicos = motor.create_df(query)
    servicos['comanda_id'] = servicos['comanda_id'].astype('int')
    events = create_events(servicos=servicos)

    st.subheader('Calendário de :grey-background[_Data de Entrega_] de Serviços :date:',)
    st.write(':large_red_square: :red[__VERMELHO: PENDENTE__] ; :large_blue_square: :blue[__AZUL: PRONTO MAS NÃO RETIRADO__];:large_green_square: :green[__VERDE: SERVIÇO RETIRADO__]')


    # calendar_options = {
    #     "headerToolbar": {
    #         "left": "today prev,next",
    #         "center": "title"
    #     }
    # }
    calendar_events = events

    selected_event = calendar(events=calendar_events,
                              callbacks='eventClick'
                            #   options=calendar_options
                              )
    if selected_event:
        base = selected_event['eventClick']['event']
        comanda_id = int(base['id'])
        df = servicos[(servicos['comanda_id']==comanda_id)]
        cliente_id = int(df[df['comanda_id']==comanda_id]['cliente_id'].iloc[0])
        nome_cliente = str(df[df['comanda_id']==comanda_id]['nome'].iloc[0])
        tel_cliente = int(df[df['comanda_id']==comanda_id]['tel'].iloc[0])
        servico = str(df[df['comanda_id']==comanda_id]['servico'].iloc[0])
        valor_total = df[df['comanda_id']==comanda_id]['preco_total'].iloc[0]
        sinal = df[df['comanda_id']==comanda_id]['sinal'].iloc[0]
        valor_restante = df[df['comanda_id']==comanda_id]['valor_restante'].iloc[0]
        format_data = '%d-%m-%Y'
        data_entrada = datetime.strptime(df[df['comanda_id']== comanda_id]['data_entrada'].iloc[0], format_data)
        data_entrega = datetime.strptime(df[df['comanda_id']== comanda_id]['data_entrega'].iloc[0], format_data)
        data_retirada = datetime.strptime(df[df['comanda_id']== comanda_id]['data_retirada'].iloc[0], format_data)
        status_name = df[df['comanda_id']==comanda_id]['status_name'].iloc[0]

        col3,col4 = st.columns([.7,.3])
        with col3:
        #5 - alterar servico:
            servico_input = st.text_input('Serviço:', value = servico)
            #6 - alterar valor_total:
            valor_total_input = st.number_input('Valor Total:', format="%.2f",value=valor_total)
            #7 - alterar sinal:
            sinal_input = st.number_input('Sinal:', format="%.2f",value=sinal)
            #8 - alterar valor_total:
            valor_restante_input = st.number_input('Valor Restante:', format="%.2f",value=valor_restante)
            #9 - alterar data entrada:
            data_entrada_input = st.date_input('Data de Entrada:', format='DD/MM/YYYY', value=data_entrada).strftime('%d-%m-%Y')
            #10 - alterar data entrega:
            data_entrega_input = st.date_input('Data de Estimada de Entrega:', format='DD/MM/YYYY', value=data_entrega).strftime('%d-%m-%Y')
            #11 - alterar data retirada:
            data_retirada_input = st.date_input('Data de retirada:', format='DD/MM/YYYY', value=data_retirada).strftime('%d-%m-%Y')

        #12 - alterar status:
            status_input = status_name

            if status_input == 'RETIRADO':
                opcoes_pag = ['DINHEIRO','PIX','CRÉDITO','DÉBITO']
                tipo_pag = st.selectbox('TIPO', opcoes_pag)
        with col4:
            if servico_input != servico:
                # st.write(f':red[__ALTERADO!__] __valor original__: {servico}')
                st.text_input(':red[__ALTERADO! :warning: descrição de serviço original:__] ',servico, disabled=True)
            else:
                st.text_input('Serviço Original: ',servico, disabled=True)

            if valor_total_input != valor_total:
                st.text_input(':red[__ALTERADO! :warning: valor total original:__] ',valor_total, disabled=True)
            else:
                st.text_input('Total Original: ',valor_total, disabled=True)

            if sinal_input != sinal:
                st.text_input(':red[__ALTERADO! :warning: sinal original:__] ',sinal, disabled=True)
            else:
                st.text_input('Sinal Original: ',sinal, disabled=True)

            if valor_restante_input != valor_restante:
                st.text_input(':red[__ALTERADO! :warning: valor restante original:__] ',valor_restante, disabled=True)
            else:
                st.text_input('Restante Original: ',valor_restante, disabled=True)

            if data_entrada_input != data_entrada.strftime(format= '%d-%m-%Y'):
                st.text_input(':red[__ALTERADO! :warning: data entrada original:__] ',data_entrada.strftime(format= '%d-%m-%Y'), disabled=True)
            else:
                st.text_input('Entrada Original: ',data_entrada.strftime(format= '%d-%m-%Y'), disabled=True)

            if data_entrega_input != data_entrega.strftime(format= '%d-%m-%Y'):
                st.text_input(':red[__ALTERADO! :warning: data entrega original:__] ',data_entrega.strftime(format= '%d-%m-%Y'), disabled=True)
            else:
                st.text_input('Entrega Original: ',data_entrega.strftime(format= '%d-%m-%Y'), disabled=True)

            if data_retirada_input != data_retirada.strftime(format= '%d-%m-%Y'):
                st.text_input(':red[__ALTERADO! :warning: data retirada original:__] ',data_retirada.strftime(format= '%d-%m-%Y'), disabled=True)
            else:
                st.text_input('Retirada Original: ',data_retirada.strftime(format= '%d-%m-%Y'), disabled=True)

            if status_input != status_name:
                st.text_input(':red[__ALTERADO! :warning: status original:__] ',status_name, disabled=True)
            else:
                st.text_input('Status Original: ', status_name, disabled=True)