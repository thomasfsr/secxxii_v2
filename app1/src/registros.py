import streamlit as st
from connectdb_sqlite import Sqlite_db
import pandas as pd
from datetime import datetime
import time


def app():
    motor = Sqlite_db()
    motor.connect()
    st.subheader('Adicionar Registro 	:moneybag:')
    with st.form('registro-form'):
        cat = ['ENTRADA', 'SAÍDA']
        tipo = ['DINHEIRO','PIX','CRÉDITO','DÉBITO']
        cat_input = st.selectbox('Tipo de registro: ', cat, index =1)
        valor_input = st.number_input('Valor: ', format="%.2f")
        tipo_pag_input = st.selectbox('tipo de transição: ',tipo)
        desc_input = st.text_input('Descrição: ')
        cliente_id_input = 'N/A'
        comanda_id = 0
        status_name = 'N/A'
        data_entrada = datetime.now().strftime('%d-%m-%Y')
        confirmar = st.form_submit_button('Confirmar')
        if confirmar:
            if cat_input == 'SAÍDA':
                valor_input = -valor_input
            try:
                motor.execute_query('''insert into registros (
                                        valor,
                                        data_entrada,
                                        comanda_id,
                                        cliente_id,
                                        status_name,
                                        tipo_pag,
                                        categoria,
                                        descricao)
                                values (?,?,?,?,?,?,?,?)
                            ''', parameters=(
                                valor_input,
                                data_entrada,
                                int(comanda_id),
                                str(cliente_id_input),
                                str(status_name),
                                str(tipo_pag_input),
                                str(cat_input),
                                str(desc_input)
                            ))
                st.success("Registrado.")
                time.sleep(2)
                st.rerun()
            except ValueError as e:
                st.error(e)
    # df = motor.create_df('select * from registros')
    # total =df['valor'].sum()
    # st.write(total)
    # st.dataframe(df.sort_index(ascending=False))
    st.divider()
    st.subheader('Consultar Registros :mag:')

    # Fetch data from the database
    df = motor.create_df('''SELECT r.*,
                           c.nome
                           FROM registros r 
                           left join clientes c on 
                           c.cliente_id = r.cliente_id''')

    now = datetime.now()
    current_day = int(now.strftime('%d'))
    current_month = int(now.strftime('%m'))
    current_year = int(now.strftime('%Y'))
    # # Convert data_entrada to datetime format if it's not already
    if not df.empty:
        df['data_entrada'] = pd.to_datetime(df['data_entrada'])
        year_options = range(df['data_entrada'].dt.year.min(), df['data_entrada'].dt.year.max() + 1)
        year_options.index(current_year)
    #     # Filter by month and year using Streamlit widgets

        selected_day = st.selectbox('Selecione Dia:', range(1, 32),index = current_day-1)
        selected_month = st.selectbox('Selecione Mês:', range(1, 13),index = current_month-1)
        selected_year = st.selectbox('Selecione Ano:', range(df['data_entrada'].dt.year.min(), df['data_entrada'].dt.year.max() + 1))

        # filtered_df = df[(df['data_entrada'].dt.month == selected_month) & (df['data_entrada'].dt.year == selected_year)]
        
        filtered_df = df[(df['data_entrada'].dt.day == selected_day) & (df['data_entrada'].dt.month == selected_month) & (df['data_entrada'].dt.year == selected_year)]
        
    #     # Calculate cumulative sum
        filtered_df['valor_acumulado'] = filtered_df['valor'].cumsum()
        valor_acumulado = filtered_df['valor'].sum()
        valor_acumulado_positivo = filtered_df[filtered_df['categoria']=='ENTRADA']['valor'].sum()
        valor_acumulado_negativo = filtered_df[filtered_df['categoria']=='SAÍDA']['valor'].sum()
        filtered_df['data_entrada'] = filtered_df['data_entrada'].dt.strftime('%d-%m-%Y')

        filtered_df = filtered_df.rename(columns={'valor': 'valor (R$)', 'valor_acumulado': 'valor_acumulado (R$)'})
        
        teste = st.dataframe(filtered_df.sort_index(ascending=False), 
                     use_container_width=True, 
                     hide_index=True, 
                     on_select='rerun',
                     selection_mode='multi-row')
        reg_idx = teste['selection']['rows']
        if reg_idx:
            reg_ids = filtered_df['registro_id'].sort_index(ascending=False).iloc[reg_idx]
            st.text(reg_ids.to_list())
            with st.popover('Deletar Registros?'):
                st.write('deseja deletar registros selecionados?')
                del_b = st.button(':red[DELETAR]')
                if del_b:
                    placeholders = ','.join('?' for _ in reg_ids)
                    motor.execute_query(f"DELETE FROM registros WHERE registro_id IN ({placeholders})",parameters=tuple(reg_ids))
                    time.sleep(1)
                    st.rerun()
        else:
            pass


        st.write(f'VALOR ACUMULADO DO DIA: R$ {valor_acumulado}')
        st.write(f':green[ Valor de ENTRADA do DIA: R$ {valor_acumulado_positivo} ]')
        st.write(f':red[ Valor de SAÍDA do DIA: R$ {valor_acumulado_negativo} ]')
        # Feature de filtrar por Cliente
        st.divider()
        st.subheader('Registro por Cliente :sleuth_or_spy:')

        all_clients = df.copy().sort_index(ascending=False)
        all_clients['id_nome'] = df['cliente_id'].astype(str) + ' - ' + df['nome']
        unique_clients = all_clients['id_nome'].unique()
        select_client = st.selectbox('Selecione Cliente:', unique_clients)
        df_cliente = df[df['cliente_id']==select_client.split(' - ')[0]]
        df_cliente['data_entrada']=df_cliente['data_entrada'].dt.strftime('%d-%m-%Y')
        df_cliente['valor_acumulado']=df_cliente['valor'].cumsum()
        valor_total_acumulado = df_cliente['valor'].sum()
        df_cliente['Tipo de Transação'] = df['status_name'].apply(lambda x: 'SINAL' if x == 'A FAZER' else 'PAGAMENTO RESTANTE')
        df_cliente = df_cliente.rename(columns={'valor': 'valor (R$)', 'valor_acumulado': 'valor_acumulado (R$)'})
        ordem = ['registro_id', 'data_entrada', 'comanda_id', 'cliente_id', 'nome', 'Tipo de Transação' , 'valor (R$)', 'valor_acumulado (R$)']
        st.dataframe(df_cliente[ordem],use_container_width=True, hide_index=True)
        st.write(f'VALOR ACUMULADO DO CLIENTE: R$ {valor_total_acumulado}')
    
    else:
        st.write('Sem dados')
        st.dataframe(df,use_container_width=True, hide_index=True)