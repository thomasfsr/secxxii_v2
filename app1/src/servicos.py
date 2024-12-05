import streamlit as st
from datetime import datetime
from connectdb_sqlite import Sqlite_db
from PIL import Image
import os
import time
from comanda_to_doc import Comanda_text
import pandas as pd


def app():
    motor = Sqlite_db()
    motor.connect()
    st.subheader('Serviços Registrados :mag:')
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
            c.tipo_pag,
            c.status_name
    from comandas c
    join clientes cl on cl.cliente_id = c.cliente_id;
    '''
    # carregar dados necessários
    servicos = motor.create_df(query)

    servicos['comanda_id'] = servicos['comanda_id'].astype('int')

    status_options = ['A FAZER', 'PRONTO', 'RETIRADO']
    s1, _ = st.columns([1,2])
    with s1:
            selected_status = st.radio("Selecione o Status:", status_options)
    
    #filtro select status:
    if selected_status == 'A FAZER':
        df = servicos[(servicos['status_name']=='A FAZER')]
    elif selected_status == 'PRONTO':
        df = servicos[(servicos['status_name']=='PRONTO')]
    elif selected_status == 'RETIRADO':
        df = servicos[(servicos['status_name']=='RETIRADO')]
    else:
        df = servicos
    
    df = df.sort_index(ascending=False)
    df['data_entrada'] = pd.to_datetime(df['data_entrada'],format='%d-%m-%Y').dt.strftime('%d-%m-%Y')
    df['data_entrega'] = pd.to_datetime(df['data_entrega'],format='%d-%m-%Y').dt.strftime('%d-%m-%Y')
    df['data_retirada'] = pd.to_datetime(df['data_retirada'],format='%d-%m-%Y').dt.strftime('%d-%m-%Y')
    # df['data_entrada'] = df['data_entrada'].dt.strftime('%d-%m-%Y')
    # df['data_entrega'] = df['data_entrega'].dt.strftime('%d-%m-%Y')
    # df['data_retirada'] = df['data_retirada'].dt.strftime('%d-%m-%Y')
    df_show = df[['comanda_id',
                  'nome',
                  'tel',
                  'servico',
                  'tipo_pag',
                  'preco_total',
                  'sinal',
                  'valor_restante',
                  'data_entrada',
                  'data_entrega',
                  'status_name'
                  ]].sort_index(axis=0, ascending=False)
    st.write('__Tabela de Comandas:__')
    id_from_df = st.dataframe(df_show, use_container_width=True, hide_index=True,height=200,
                 on_select='rerun',
                 selection_mode='single-row')
    try:
        idx_df = id_from_df['selection']['rows'][0]
    except:
        idx_df = 0
        pass

    if not df.empty:
        # df['options'] = 'Nº COMANDA (' + df['comanda_id'].astype(str) +'): ' + df['nome'] + ' | SERVIÇO: ' + df['servico'] + ' | STATUS: ' + df['status_name']
        # #Form:
        # #1 - filtrar por comanda
        # option = st.selectbox('Escolha uma comanda para atualizar:', df['options'],label_visibility='collapsed')
        
        # st.subheader('Dados da Comanda:')
        # #2 - carregar dados da comanda
        # comanda_id = option.split(')')[0]
        # comanda_id = int(comanda_id.split('(')[1])
        comanda_id = int(df['comanda_id'].iloc[idx_df])
        
        cliente_id = int(df[df['comanda_id']==comanda_id]['cliente_id'].iloc[0])
        
        nome_cliente = str(df[df['comanda_id']==comanda_id]['nome'].iloc[0])
        
        tel_cliente = int(df[df['comanda_id']==comanda_id]['tel'].iloc[0])
        
        servico = str(df[df['comanda_id']==comanda_id]['servico'].iloc[0])
        
        tipo_pag = str(df[df['comanda_id']==comanda_id]['tipo_pag'].iloc[0])

        valor_total = df[df['comanda_id']==comanda_id]['preco_total'].iloc[0]
        
        sinal = df[df['comanda_id']==comanda_id]['sinal'].iloc[0]
        valor_restante = df[df['comanda_id']==comanda_id]['valor_restante'].iloc[0]
        format_data = '%d-%m-%Y'
        data_entrada = datetime.strptime(df[df['comanda_id']== comanda_id]['data_entrada'].iloc[0], format_data)
        data_entrega = datetime.strptime(df[df['comanda_id']== comanda_id]['data_entrega'].iloc[0], format_data)
        data_retirada = datetime.strptime(df[df['comanda_id']== comanda_id]['data_retirada'].iloc[0], format_data)
        status_name = df[df['comanda_id']==comanda_id]['status_name'].iloc[0]
        
        clientes = motor.create_df('select * from clientes')
        clientes['id_e_nome_tel'] = 'CLIENTE ID (' + clientes['cliente_id'].astype('str') + '): ' + clientes['nome'] + ' | TEL: ' + clientes['tel'].astype('int64').astype('str')
        idx_cl = clientes[clientes['cliente_id']==cliente_id].index
        idx_cl = int(idx_cl[0])
        s11, _ = st.columns(2)
        with s11:
            cliente_input = st.selectbox('**Cliente:**', clientes['id_e_nome_tel'], index=idx_cl)
        cliente_input = cliente_input.split(')')[0]
        cliente_input = int(cliente_input.split('(')[1])

        with st.popover('Alterar Dados de Cliente'):
            nome_cliente_input = st.text_input('Alterar nome:',value=nome_cliente)
            tel_input = st.text_input('Alterar tel:', max_chars=11, value=tel_cliente)
            save_alt = st.button(':blue[**SALVAR ALTERAÇÃO DE CLIENTE**] :floppy_disk:')
            if save_alt:
                if len(tel_input) < 11:
                        st.error('Telefone deve conter 11 dígitos')
                        time.sleep(1)
                        st.rerun()
                if not tel_input.isdigit():
                        st.error('Telefone aceita SOMENTE NÚMEROS.')
                        time.sleep(1)
                        st.rerun()
                try:
                    motor.execute_query('''
                                    UPDATE clientes
                                    SET nome = ?,
                                    tel = ?
                                    WHERE cliente_id = ?
                                    ''',
                                    (nome_cliente_input, 
                                        tel_input,
                                        cliente_id
                                    ))
                    st.success('Cliente Atualizado com Sucesso!')
                    time.sleep(1)
                    motor.close()
                    st.rerun()
                except ValueError as e:
                    st.error(f'não foi possivel cadastrar!{e}')
                    time.sleep(1)
                    motor.close()
                    st.rerun()

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
            #12 - tipo de pagamento:
            opcoes_pag = ['DINHEIRO','PIX','CRÉDITO','DÉBITO','vazio']
            idx_tipo_pag = opcoes_pag.index(tipo_pag)
            tipo_pag_input = st.selectbox('Tipo de Pagamento da entrada: ', opcoes_pag, index=idx_tipo_pag)
            #13 - alterar status:
            idx_status = status_options.index(status_name)
            status_input = st.selectbox('Status:',status_options,index= idx_status)

            if status_input == 'RETIRADO':
                opcoes_pag = ['DINHEIRO','PIX','CRÉDITO','DÉBITO', 'vazio']
                tipo_pag = st.selectbox('Tipo de Pagamento Restante: ', opcoes_pag, index=4)
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

            # if status_input != status_name:
            #     st.text_input(':red[__ALTERADO! :warning: status original:__] ',status_name, disabled=True)
            # else:
            #     st.text_input('Status Original: ', status_name, disabled=True)

        col1, col2 = st.columns(2)
        with col1:
            update_button = st.button('**:blue[SALVAR ATUALIZAÇÃO] :floppy_disk:**')
            if update_button:
                if status_input == 'RETIRADO' and valor_restante_input >0:
                    #update Registro
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
                                    ''',parameters=(valor_restante_input,
                                                    datetime.now().strftime('%d-%m-%Y'),
                                                    comanda_id, 
                                                    cliente_id,
                                                    status_input, 
                                                    tipo_pag,
                                                    'ENTRADA',
                                                    'pagamento de cliente'
                                                    ))
                    categoria = 'QUITAÇÃO DE SERVIÇO'
                    motor.execute_query('''insert into fluxo (
                                            valor,
                                            data_entrada,
                                            categoria,
                                            comanda_id)
                                    values (?,?,?,?)
                                    ''',parameters=(valor_restante_input,
                                                    datetime.now().strftime('%d-%m-%Y'),
                                                    categoria,
                                                    comanda_id))
                # fim do "IF RETIRADO".
                #update log de comanda:
                motor.execute_query(f'''
                        INSERT INTO log_comandas (
                                    comanda_id,
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
                            cliente_id,
                            datetime.now().strftime('%d-%m-%Y'),
                            servico,
                            valor_total_input,
                            sinal_input,
                            valor_restante_input,
                            status_input)
                            )
                # Atualizar tabela comanda:
                motor.execute_query('''update comandas set 
                                cliente_id = ?,
                                data_entrada = ?,
                                data_entrega = ?, 
                                data_retirada = ?,
                                servico = ?,
                                preco_total = ?,
                                sinal = ?,
                                valor_restante = ?,
                                status_name = ?

                                WHERE comanda_id = ?
                                ;''',
                                (cliente_input,
                                data_entrada_input,
                                data_entrega_input,
                                data_retirada_input,
                                servico_input,
                                valor_total_input,
                                sinal_input,
                                valor_restante_input,
                                status_input,
                                comanda_id
                                ))
                st.success("Comanda Atualizada! :smile:")
                time.sleep(1)
                motor.close()
                st.rerun()
            with st.popover(':red[**Excluir Comanda**] :wastebasket:'):
                deletar_comanda = st.button(':red[**Excluir definitivamente a comanda?**] :fire:')
                if deletar_comanda:
                    motor.execute_query(f'DELETE FROM comandas WHERE comanda_id = {int(comanda_id)};')
                    motor.execute_query(f'DELETE FROM registros WHERE comanda_id = {int(comanda_id)};')
                    st.success('Comanda Deletada.')
                    motor.close()
                    st.rerun()
        with col2:
        #doc button:
            docx = Comanda_text(cliente=str(nome_cliente),tel=str(tel_cliente),
                                     servico=str(servico), valor_total='R$ ' + str(valor_total),
                                     data_entrada=str(data_entrada.strftime('%d-%m-%Y')),
                                     data_retirada=str(data_retirada.strftime('%d-%m-%Y')),sinal='R$ ' + str(sinal),
                                     restante='R$ '  + str(valor_restante),comanda_id= str(comanda_id))
            doc_buffer = docx.text()
            doc_filename = f"comanda_{str(nome_cliente)}_{str(comanda_id)}.docx"
            download_comanda_button = st.download_button('**Download da Comanda** :receipt:',
                                                    data=doc_buffer,
                                                    file_name= doc_filename,
                                                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            if download_comanda_button:
                st.success('Download da comanda concluído! :white_check_mark:')
        #imagem:
            image_path = f'data/images/{str(comanda_id)}_{nome_cliente}_image.jpeg'
            if os.path.exists(image_path):
                st.write('Foto do serviço:')
                st.image(image_path, width=300,caption=f'{image_path}')
                excluir_foto = st.button(':red[Excluir foto?]')
                if excluir_foto:
                    os.remove(image_path)
                    st.success('Foto deletada.')
                    time.sleep(1)
                    st.rerun()

            else:
                st.warning("Comanda sem imagem anexada.")
                uploaded_file = st.file_uploader("Deseja anexar foto?", type=["jpg", "jpeg", "png"],accept_multiple_files=False)
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    os.makedirs('data/images', exist_ok=True)
                    save_path = f'data/images/{str(comanda_id)}_{nome_cliente}_image.jpeg'
                    image.save(save_path)
                    st.success(f"Imagem foi salva com sucesso :smile:: {save_path}")
                    time.sleep(1)
                    st.rerun()