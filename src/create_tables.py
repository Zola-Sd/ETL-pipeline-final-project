"""
A module containing the script
to create the tables in the db
with the correct PK and FK
assignments
"""
#TODO: Maybe rename this to db_manager.py Handle the engine objects here for dataframes?
import psycopg2 
from sqlalchemy import create_engine

#postgreSQL connection for creating tables + queries to populate tables with FKs
def fetch_conn():
    conn = psycopg2.connect(
        host="localhost",
        user="root",
        password="password",
        database="postgres"
    )

    return conn

#sqlalchemy connection from engine object (for loading dfs)
def fetch_eng_conn():
    conn_string = 'postgresql://root:password@localhost/postgres'

    db = create_engine(conn_string)
    conn = db.connect()

    return conn

#BRANCH TABLE
def create_branch_table():
    conn = fetch_conn()
    cursor = conn.cursor()

    sql = \
        """
        CREATE TABLE IF NOT EXISTS branches(
            branch_id SERIAL PRIMARY KEY NOT NULL,
            branch_name VARCHAR NOT NULL
        );
        """
    
    cursor.execute(sql)
    conn.commit()
    conn.close()

#CUSTOMER TABLE
def create_customer_table():
    conn = fetch_conn()
    cursor = conn.cursor()

    #cust_card can be NULL if the payment type was CASH
    sql = \
        """
        CREATE TABLE IF NOT EXISTS customers(
            cust_id SERIAL PRIMARY KEY NOT NULL,
            cust_name VARCHAR NOT NULL,
            cust_card VARCHAR
        );
        """

    cursor.execute(sql)
    conn.commit()
    conn.close()

#PRODUCTS TABLE
def create_products_table():
    conn = fetch_conn()
    cursor = conn.cursor()

    sql = \
        """
        CREATE TABLE IF NOT EXISTS products(
            product_id SERIAL PRIMARY KEY NOT NULL,
            product_name VARCHAR NOT NULL,
            product_flavour VARCHAR NOT NULL,
            product_price FLOAT NOT NULL
        );
        """
    
    cursor.execute(sql)
    conn.commit()
    conn.close()

#ORDERS TABLE
def create_orders_table():
    conn = fetch_conn()
    cursor = conn.cursor()

    sql = \
        """
        CREATE TABLE IF NOT EXISTS orders(
            order_id SERIAL PRIMARY KEY NOT NULL,
            time_stamp VARCHAR NOT NULL,
            branch_id INT NOT NULL,
            cust_id INT NOT NULL,
            payment_type VARCHAR NOT NULL,
            total_price FLOAT NOT NULL,
            
            CONSTRAINT fk_branch_id 
            FOREIGN KEY (branch_id)
            REFERENCES branches(branch_id),

            CONSTRAINT fk_cust_id
            FOREIGN KEY (cust_id)
            REFERENCES customers(cust_id)
        );
        """

    cursor.execute(sql)
    conn.commit()
    conn.close()

#BASKET TABLE
def create_basket_table():
    conn = fetch_conn()
    cursor = conn.cursor()

    sql = \
        """
        CREATE TABLE IF NOT EXISTS basket(
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            
            CONSTRAINT fk_order_id
            FOREIGN KEY (order_id)
            REFERENCES orders(order_id),

            CONSTRAINT fk_product_id
            FOREIGN KEY (product_id)
            REFERENCES products(product_id)
        );
        """

    cursor.execute(sql)
    conn.commit()
    conn.close()

#CREATE TABLES
create_branch_table()
create_customer_table()
create_products_table()
create_orders_table()
create_basket_table()

