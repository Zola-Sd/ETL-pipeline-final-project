import norm_data as n
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.types import VARCHAR, INTEGER, Integer, Float

conn_string = 'postgresql://root:password@localhost/postgres'

#Create engine and connection objects
db = create_engine(conn_string)
# print(db)
connection = db.connect()
# print(connection)

#Create connection and cursor objects
# connection = ss.fetch_connection()
# cursor = connection.cursor()

#Store dfs 
store_df = n.store_table()
items_df = n.items_table()
cust_df = n.customer_table()
trans_df = n.trans_table()
basket_df = n.basket_table()

def load_stores():
    store_df.to_sql('store_table', con=connection, if_exists='append', index_label='branch_id')
                    # index=True, index_label='branch_id')
                    # dtype={
                    #     'branch_id': Integer(),
                    #     'branch_name': VARCHAR(),
                    #     'branch_code': VARCHAR(),
                    # })

    conn = psycopg2.connect(conn_string)
    conn.commit()

    #ALTER TABLE to reassign Keys?

def load_cust():
    cust_df.to_sql('cust_table', con=connection, if_exists='append',index_label='cust_id')
                    # index=True, index_label='branch_id')
                    # dtype={
                    #     'branch_id': Integer(),
                    #     'branch_name': VARCHAR(),
                    #     'branch_code': VARCHAR(),
                    # })
    conn = psycopg2.connect(conn_string)
    conn.commit()
    
def load_items():
    items_df.to_sql('items_table', con=connection, if_exists='append',
                    index=True, index_label='item_id')
                    # dtype={
                    #     'item_id': Integer(),
                    #     'item_name': VARCHAR(),
                    #     'item_price': Float(),
                    #     'flavour': VARCHAR()
                    # })
    conn = psycopg2.connect(conn_string)
    conn.commit()

def load_trans():
    trans_df.to_sql('transactions_table', con=connection, if_exists='append',
                    index=True, index_label='trans_id',
                    dtype={
                        'trans_id': Integer(),
                        'order_id': Integer(),
                        'time_stamp': VARCHAR(),
                        'branch_id': Integer(),
                        'cust_id': Integer(),
                        'payment_method': VARCHAR(),
                        'total_price': Float()
                    })
    conn = psycopg2.connect(conn_string)
    conn.commit()

def load_basket():
    basket_df.to_sql('basket_table', con=connection,
                     if_exists='append', index=True, index_label='order_id')
    conn = psycopg2.connect(conn_string)
    conn.commit()

load_stores()
load_cust()
load_items()
load_trans()
load_basket()