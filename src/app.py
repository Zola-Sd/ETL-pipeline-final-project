"""
A module handling the loading
of transformed dfs into the db.
TODO: Maybe rename this file/restructure modules
so that everything can be run inside a run_app() function
which is then passed into the lambda_handler()
"""

import create_tables as ct
import transform as tr

branches_df = tr.create_branches_df()
customers_df = tr.create_customer_df()
products_df = tr.create_products_df()

def load_stores():
    branches_df.to_sql('branches', con=ct.fetch_eng_conn(), if_exists='append', index_label='branch_id')

    conn = ct.fetch_conn()
    conn.commit()
    conn.close()

def load_customers():
    customers_df.to_sql('customers', con=ct.fetch_eng_conn(), if_exists='append',index_label='cust_id')
                    
    conn = ct.fetch_conn()
    conn.commit()
    conn.close()
    
def load_products():
    products_df.to_sql('products', con=ct.fetch_eng_conn(), if_exists='append', index_label='product_id')
                    
    conn = ct.fetch_conn()
    conn.commit()
    conn.close()

def load_orders(orders_df):
    orders_df.to_sql('orders', con=ct.fetch_eng_conn(), if_exists='append', index_label='order_id')

    conn = ct.fetch_conn()
    conn.commit()
    conn.close()

def load_basket(basket_df):
    basket_df.to_sql('basket', con=ct.fetch_eng_conn(), if_exists='append', index=False)

    conn = ct.fetch_conn()
    conn.commit()
    conn.close()

#These tables must be loaded first
def first_load():
    load_stores()
    load_customers()
    load_products()

#These are loaded after as the FKs depend on this data in the database
def second_load():
    orders_df = tr.create_orders_df()
    load_orders(orders_df)
    basket_df = tr.create_basket_df()
    load_basket(basket_df)
    
first_load()
second_load()