import streamlit as st
from connectdb_sqlite import Sqlite_db
import pandas as pd
from datetime import datetime
import time


def app():
    motor = Sqlite_db()
    motor.connect()
    st.subheader('Checagem de Serviços com :gray-background[_Data de Entrega_] até a Data Atual 	:file_folder:')

    query = '''
    select c.comanda_id,
            c.data_retirada,
            c.cliente_id,
            cl.nome,
            cl.tel,
            c.servico,
            c.preco_total,
            c.sinal,
            c.valor_restante,
            c.tipo_pag,
            c.status_name
    from comandas c
    join clientes cl on cl.cliente_id = c.cliente_id
    WHERE status_name != 'RETIRADO' AND data_retirada <= strftime('%d-%m-%Y', 'now');
    '''

    df = motor.create_df(query=query)
    df['data_retirada']= pd.to_datetime(df['data_retirada'],format='%d-%m-%Y')
    df = df.sort_values(by='data_retirada', ascending=False)
    df['data_retirada'] = df['data_retirada'].dt.strftime('%d-%m-%Y')
    selection = st.dataframe(df,on_select='rerun',
                 selection_mode='multi-row', hide_index=True)
    servico_idx = selection['selection']['rows']
    if servico_idx:
        button_update = st.button('FINALIZAR PEDIDOS :white_check_mark:',use_container_width=True)
        servico_ids = df['comanda_id'].sort_index(ascending=False).iloc[servico_idx]
        placeholders = ','.join('?' for _ in servico_ids)

        if button_update:
            motor.execute_query(f'''UPDATE comandas 
                                set status_name = "RETIRADO"
                                WHERE comanda_id IN ({placeholders})
                                ''',parameters=tuple(servico_ids))
            st.success('Serviços Finalizados com Sucesso')
            time.sleep(1)
            st.rerun()
            
            # Handling the table registro:

            motor.execute_query(
                 f'''insert into registros (valor,data_entrada,comanda_id,cliente_id,status_name,tipo_pag,categoria,descricao)
                 select c.valor_restante, strftime('%d-%m-%Y', 'now'), r.comanda_id, r.cliente_id, "RETIRADO", r.tipo_pag, "ENTRADA", r.descricao from registros r
                 join comandas c on c.comanda_id = r.comanda_id
                 WHERE r.comanda_id in ({placeholders})''', parameters = tuple(servico_ids))