import streamlit as st
import time
from PIL import Image
import os

from comanda_to_doc import Comanda_text
from connectdb_sqlite import Sqlite_db

def app():
    motor = Sqlite_db()
    motor()
    motor.connect()

    opcoes_pag = ['DINHEIRO','PIX','CRÉDITO','DÉBITO']
    clientes = motor.create_df('SELECT * FROM clientes')
    
    #clientes['id_and_nome_tel'] = 'CLIENTE ID (' + clientes['cliente_id'].astype(str) + '): ' + clientes['nome'] + ' | TEL: ' + clientes['tel'].astype('int64').astype('str')
    clientes = clientes.sort_index(ascending=False)
    st.subheader('Cadastrar Nova Comanda :memo:')

    c1, c2, c3 = st.columns([1,1,2])
    #Cadastrar cliente novo? 
    with c1:
        with st.popover('**:blue[Cadastrar Novo Cliente?]** :woman-raising-hand:'):
            nome = st.text_input('Nome:',placeholder="Digite o nome do novo cliente")
            telefone = st.text_input('Telefone:', max_chars=11,placeholder="13987654321")
            button_cadastrar = st.button('Cadastrar')
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
                    st.rerun()
                
                except ValueError as e:
                    st.error(f'não foi possivel cadastrar!{e}')
                    time.sleep(1)
                motor.close()
                st.rerun()

    with c2:
        with st.popover('**Selecionar Cliente Cadastrado? 	:handshake:**'):
            st.write('__Tabela de Clientes:__')
            id_clientes = st.dataframe(clientes, use_container_width=False, hide_index=True,height=200, width=500,
                        on_select='rerun',
                        selection_mode='single-row')
    try:
        idx_cliente = id_clientes['selection']['rows'][0]
    except:
        idx_cliente = 0
        pass
    s1, _ = st.columns([2,4])
    with s1:
        cliente_input = st.text_input('Cliente: ', str(clientes['cliente_id'].iloc[idx_cliente]) + ' - ' + str(clientes['nome'].iloc[idx_cliente]),
                                      disabled=True)
    # cliente_input = st.selectbox('Selecione Cliente:', clientes['id_and_nome_tel'])
    
    servico_input = st.text_input('Descrição do Serviço:',placeholder="Digite o serviço a ser prestado aqui")

    s11, s12, s13, s14 = st.columns([2,2,2,2])
    with s11:
        data_entrada_input_dt = st.date_input('Data de Entrada:', format='DD/MM/YYYY')
        data_entrada_input = data_entrada_input_dt.strftime('%d-%m-%Y')
        valor_total_input = st.number_input('Valor Total:', format="%.2f")       
        tipo_pag = st.selectbox('Tipo de Pagamento',opcoes_pag)
        status_input = 'A FAZER'
    with s12:
        data_entrega_input_dt = st.date_input('Data Estimada de Entrega:', format='DD/MM/YYYY')
        data_entrega_input = data_entrega_input_dt.strftime('%d-%m-%Y')
        sinal_input = st.number_input('Sinal:', format="%.2f")
    restante = valor_total_input - sinal_input

    with s13:
        days = data_entrega_input_dt - data_entrada_input_dt
        st.text_input('Número de dias para entregar:', f'{str(days.days)} dias', disabled=True)
        st.text_input('Valor Restante:', f'R$ {str(restante)}', disabled=True)

    col1, col2 = st.columns([2,1])
    with col1:
        button_comanda = st.button('**:blue[SALVAR COMANDA ]** :floppy_disk:')
    with col2:
        uploaded_file = st.file_uploader("Insira foto se desejar", type=["jpg", "jpeg", "png"],accept_multiple_files=False)

    if button_comanda: 
        # cliente_input = cliente_input.split(')')[0]
        # cliente_input = cliente_input.split('(')[1]
        # cliente_input = int(cliente_input)
        cliente_input = int(clientes['cliente_id'].iloc[idx_cliente])
        try:
            motor.execute_query(f'''
                            INSERT INTO comandas (
                                cliente_id,
                                data_entrada,
                                data_entrega,
                                data_retirada,
                                servico,
                                preco_total,
                                sinal,
                                valor_restante,
                                tipo_pag,
                                status_name)
                            VALUES (?,?,?,?,?,?,?,?,?,?)''', 
                            parameters=(
                            cliente_input, 
                            data_entrada_input,
                            data_entrega_input,
                            data_entrega_input,
                            servico_input,
                            valor_total_input,
                            sinal_input,
                            restante,
                            tipo_pag,
                            status_input))
        except ValueError as e:
            st.error(f'Não foi possivel cadastrar: {e}')
            st.rerun()

        #botão download comanda
        cnome = str(clientes[clientes['cliente_id']== cliente_input]['nome'].iloc[0])
        tel = clientes[clientes['cliente_id']== cliente_input]['tel'].iloc[0]
        tel = int(tel)
        dentrada = data_entrada_input
        dentrega = data_entrega_input
        comanda_id = motor.get_last_id()
        docx = Comanda_text(cliente=cnome,tel=str(tel),
                            servico=str(servico_input), valor_total='R$ ' + str(valor_total_input),
                            data_entrada=str(dentrada),
                            data_retirada=str(dentrega),sinal='R$ ' + str(sinal_input),
                            restante='R$ '  + str(restante),comanda_id= comanda_id)
        doc_buffer = docx.text()
        doc_filename = f"comanda_{str(cnome)}_{comanda_id}.docx"
        dbutton = st.download_button('**Download da Comanda** :receipt:',use_container_width=True,
            data=doc_buffer,
            file_name=doc_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        if dbutton:
            st.success('Download da comanda concluído! :white_check_mark:')
            time.sleep(1)
            motor.close()
            st.rerun()
        
        #Registro:
        if sinal_input > 0:
            try:
                motor.execute_query(f'''
                                INSERT INTO registros (
                                    valor,
                                    data_entrada,
                                    comanda_id,
                                    cliente_id,
                                    status_name,
                                    tipo_pag,
                                    categoria,
                                    descricao)
                                VALUES (?,?,?,?,?,?,?,?)
                                ''', parameters=(
                                sinal_input,data_entrada_input, comanda_id,
                                cliente_input, status_input, tipo_pag, 'ENTRADA', 'pagamento de cliente')
                                )
            except ValueError as e:
                st.error(f'Erro para registrar: {e}')

            #Fluxo
            categoria = 'SINAL'
            try:
                motor.execute_query(f'''
                                INSERT INTO fluxo (
                                    valor,
                                    data_entrada,
                                    categoria,
                                    comanda_id)
                                VALUES (?,?,?,?)
                                ''', parameters=(
                                sinal_input,
                                data_entrada_input, 
                                categoria,
                                comanda_id)
                                )
            except ValueError as e:
                st.error(f'Erro para registrar: {e}')
        #Log:
        try:
            motor.execute_query(f'''
                            INSERT INTO log_comandas (comanda_id,
                                cliente_id,
                                data_evento,
                                servico,
                                preco_total,
                                sinal,
                                valor_restante,
                                status_name)
                            VALUES (?,?,?,?,?,?,?,?)
                            ''', parameters=(
                            comanda_id, 
                            cliente_input, 
                            data_entrada_input,
                            servico_input,
                            valor_total_input,
                            sinal_input,
                            valor_total_input - sinal_input,
                            status_input)
                            )
        except ValueError as e:
            st.error(f'Error para log: {e}')

        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            os.makedirs('data/images', exist_ok=True)
            save_path = f'data/images/{comanda_id}_{cnome}_image.jpeg'
            image.save(save_path)
            st.success(f"Imagem foi salva com sucesso: {save_path}")
        else:
            st.write("Nenhuma imagem carregada.")