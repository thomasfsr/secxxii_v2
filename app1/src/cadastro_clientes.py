import streamlit as st
from connectdb_sqlite import Sqlite_db
import time

def app():

    motor = Sqlite_db()
    motor.connect()

    st.subheader('Cadastro de Cliente 	:man-raising-hand: 	:woman-raising-hand:')

    with st.form(key='cliente_form'):
        nome = st.text_input('Nome:',placeholder="Digite o nome do novo cliente")
        telefone = st.text_input('Telefone:', max_chars=11,placeholder="13987654321")

        button_cadastrar = st.form_submit_button('Cadastrar')

        if button_cadastrar:
            if len(telefone) < 11:
                st.error('Telefone deve conter 11 dígitos')
                time.sleep(1)
                st.rerun()
                
            if not telefone.isdigit():
                st.error('Telefone aceita SOMENTE NÚMEROS.')
                time.sleep(1)
                st.rerun()
            try:
                telefone = int(telefone)
                motor.execute_query('''
                        INSERT INTO clientes (nome, tel)
                        VALUES (?,?)
                        ''', (nome, telefone))
                st.success(f'{nome} cadastrado!')
                time.sleep(1)
            
            except ValueError as e:
                st.error(f'não foi possivel cadastrar!{e}')
                time.sleep(1)
            motor.close()
            st.rerun()
            
    df = motor.create_df('select * from clientes').sort_index(ascending=False)
    if not df.empty:
        st.dataframe(df,use_container_width=True, hide_index=True, height=200)
    else:
        st.error("Tabela de clientes está vazia.")
    



    st.subheader("Alterar dados de Cliente")
    df = motor.create_df('select * from clientes').sort_index(ascending=False)
    if df is not df.empty:
        df['id_cliente'] = df['cliente_id'].astype(str) + ' - ' + df['nome']
        selected_cliente = st.selectbox('Selecione um cliente:', df['id_cliente'])
        if selected_cliente is not None:
            id_sel_cliente = selected_cliente.split(' - ')[0]
            nome_c = selected_cliente.split(' - ')[1]
            tel_c = df[df['cliente_id']==int(id_sel_cliente)]['tel'].iloc[0]
            tel_c_int = int(tel_c)
            st.write(f'Telefone cadastrado de {nome_c}: {str(tel_c_int)}')
        
        nome_new = st.text_input('Alterar nome',placeholder="Digite o novo nome")

        tel_new = st.text_input('Alterar tel', max_chars=11,placeholder="13987654321")
            
        save_alt = st.button(':blue[**SALVAR ALTERAÇÃO DE DADOS DE CLIENTE**] :floppy_disk:')
    else:
        st.error('Tabela Cliente Vazia.')
    if save_alt:
        if tel_new and not nome_new:
            if len(tel_new) < 11:
                st.error('Telefone deve conter 11 dígitos')
                time.sleep(1)
                st.rerun()
                
            if not tel_new.isdigit():
                st.error('Telefone aceita SOMENTE NÚMEROS.')
                time.sleep(1)
                st.rerun()
            try:
                motor.execute_query('''
                                UPDATE clientes
                                SET tel = ?
                                WHERE cliente_id = ?
                            ''', (tel_new, id_sel_cliente ))
                st.success('Tel alterado com sucesso.')
                time.sleep(1)
                motor.close()
                st.rerun()

            except ValueError as e:
                st.error(f'não foi possivel cadastrar!{e}')
                time.sleep(1)
            st.rerun()

        if nome_new and not tel_new:
            try:
                motor.execute_query('''
                        UPDATE clientes
                        SET nome = ?
                        WHERE cliente_id = ?
                    ''', (nome_new, id_sel_cliente ))
                st.success('Nome alterado com sucesso.')
                time.sleep(1)

            except ValueError as e:
                st.error(f'não foi possivel cadastrar!{e}')
                time.sleep(1)
            motor.close()
            st.rerun()
        
        elif nome_new and tel_new:
            if len(tel_new) < 11:
                st.error('Telefone deve conter 11 dígitos')
                time.sleep(1)
                st.rerun()
                
            if not tel_new.isdigit():
                st.error('Telefone aceita SOMENTE NÚMEROS.')
                time.sleep(1)
                st.rerun()

            try:
                motor.execute_query('''
                                UPDATE clientes
                                SET nome = ?, tel = ?
                                WHERE cliente_id = ?
                            ''', (nome_new, tel_new, id_sel_cliente ))
                st.success('Nome e telefone alterados com sucesso!')
                time.sleep(1)

            except ValueError as e:
                st.error(f'não foi possivel cadastrar!{e}')
                time.sleep(1)
            motor.close()
            st.rerun()