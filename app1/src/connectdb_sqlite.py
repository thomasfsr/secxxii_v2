import sqlite3
import os
import pandas as pd
import time
# from connectdb import Motor

class Sqlite_db:

    def __init__(self, db_path:str= '.',db_name:str='secxxii_sqlite.db'):
        os.makedirs(db_path, exist_ok=True)
        self.db_path = db_path
        self.db_name = db_name
        self.con = None

    def __call__(self, sqlfile_path:str ='sql_scripts/creating_tables.sql'):
        if self.con is None:
            print("No active connection found. Establishing a connection...")
            self.connect() 
        self.create_tables(sqlfile_path)

    def connect(self):
            try:
                self.con = sqlite3.connect(f'{self.db_path}/{self.db_name}')
                print('Successfully Connected')
            except sqlite3.Error as e:
                print(f'Error connecting to database: {e}')
                print('Retrying in 5 seconds...')
                time.sleep(5)  # Wait for 5 seconds before retrying
        
    def create_tables(self, sqlfile_path:str ='sql_scripts/creating_tables.sql'):
        try:
            with open(sqlfile_path, 'r') as file:
                query = file.read()
            cursor = self.con.cursor()
            cursor.executescript(query)
            self.con.commit()
        except (sqlite3.Error, FileNotFoundError) as e:
            print(f'Error creating tables: {e}')
        finally:
            if cursor:
                cursor.close()

    def create_df(self, query:str):
        cursor = self.con.execute(query)
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=[col[0] for col in cursor.description])
        cursor.close()
        return df
    
    def execute_query(self, query:str, parameters:tuple=None):
        cursor = self.con.cursor()
        try:
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            self.con.commit()
            return cursor
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

    def insert_dataframe(self, table_name: str, df: pd.DataFrame):
        df.to_sql(table_name, self.con, if_exists='append', index=False)

    def get_last_id(self):
        try:
            cursor = self.con.cursor()
            cursor.execute("SELECT last_insert_rowid() AS last_id;")
            row = cursor.fetchone()
            last_id = row[0] if row else None
            cursor.close()
            return last_id
        except sqlite3.Error as e:
            print(f"Error fetching last_id: {e}")
            return None

    def close(self):
        if self.con:
            self.con.close()
            print("Connection Closed!")

if __name__ == '__main__':
    
    os.makedirs('data',exist_ok=True)
    # clientedf = pd.read_parquet('backup/cliente.parquet')
    # comandadf = pd.read_parquet('backup/comanda.parquet')
    # log_comandadf = pd.read_parquet('backup/log_comanda.parquet')
    # registrodf = pd.read_parquet('backup/registro.parquet')

    # Motor('database','data').con.execute('select * from cliente').fetch_df()
    # clientedf = Motor('database','data').con.execute('select * from cliente').fetch_df()
    # comandadf = Motor('database','data').con.execute('select * from comanda').fetch_df()
    # comandadf['tipo_pag'] = "vazio"
    # log_comandadf = Motor('database','data').con.execute('select * from log_comanda').fetch_df()
    # registrodf = Motor('database','data').con.execute('select * from registro').fetch_df()
    # registrodf['tipo_pag'] = 'vazio'
    # registrodf['categoria'] = 'ENTRADA'
    # registrodf['descricao'] = 'pagamento de cliente'

    # comandadf['data_entrada'] = comandadf['data_entrada'].dt.strftime('%d-%m-%Y')
    # comandadf['data_entrega'] = comandadf['data_entrega'].dt.strftime('%d-%m-%Y')
    # comandadf['data_retirada'] =comandadf['data_retirada'].dt.strftime('%d-%m-%Y')
    # log_comandadf['data_evento'] = log_comandadf['data_evento'].dt.strftime('%d-%m-%Y')
    # registrodf['data_entrada'] = registrodf['data_entrada'].dt.strftime('%d-%m-%Y')

    # motornew = Sqlite_db()
    # motornew.connect()
    # motornew.create_tables('src/sql/new_db.sql')
    # motornew.insert_dataframe('clientes', clientedf)
    # motornew.insert_dataframe('comandas', comandadf)
    # motornew.insert_dataframe('log_comandas', log_comandadf)
    # motornew.insert_dataframe('registros', registrodf)

    # df = motornew.create_df("SELECT * from clientes")
    # print(df.head())
    # motornew.close()