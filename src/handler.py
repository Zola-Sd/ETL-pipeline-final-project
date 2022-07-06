"""
A module containing the handler function
which is executed when the lambda is
triggered by the S3 event (PutObject)
"""
import db_manager as dbm
import transform as tr
import load_data as ld

def run_app(df):
    
    #Create all tables in redshift
    dbm.create_all_tables()
    
    #Transformations - returning the dfs to be loaded
    #Transformed dfs for first load
    branches_df = tr.create_branches_df(df)
    customers_df = tr.create_customer_df(df)
    products_df = tr.create_products_df(df)

    #First load needs to occur for PKs (used to populate FKs)
    ld.load_branches(branches_df)
    ld.load_customers(customers_df)
    ld.load_products(products_df)

    #Handle duplicates from values in the db
    tr.remove_duplicate_branches()
    tr.remove_duplicate_products()
    tr.remove_duplicate_customers()

    #More transformations...
    orders_df = tr.create_orders_df(df)
    basket_df = tr.create_basket_df(df)
    
    #Second load
    ld.load_orders(orders_df)
    ld.load_basket(basket_df)
    
    print("Did it work?")
    
