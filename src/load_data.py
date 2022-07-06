"""
A module handling the loading
of transformed dfs into the db.
"""
import db_manager as dbm

def load_branches(branches_df):
    branches_df.to_sql('branches', con=dbm.fetch_eng_conn(), if_exists='append', index=False, index_label='branch_id', method='multi')

    conn = dbm.fetch_conn()
    conn.commit()
    conn.close()

def load_customers(customers_df):
    customers_df.to_sql('customers', con=dbm.fetch_eng_conn(), if_exists='append', index=False, index_label='cust_id', method='multi')
                    
    conn = dbm.fetch_conn()
    conn.commit()
    conn.close()
    
def load_products(products_df):
    products_df.to_sql('products', con=dbm.fetch_eng_conn(), if_exists='append', index=False, index_label='product_id', method='multi')
                    
    conn = dbm.fetch_conn()
    conn.commit()
    conn.close()

def load_orders(orders_df):
    orders_df.to_sql('orders', con=dbm.fetch_eng_conn(), if_exists='append', index=False, index_label='order_id', method='multi')

    conn = dbm.fetch_conn()
    conn.commit()
    conn.close()

def load_basket(basket_df):
    basket_df.to_sql('basket', con=dbm.fetch_eng_conn(), if_exists='append', index=False, method='multi')

    conn = dbm.fetch_conn()
    conn.commit()
    conn.close()
