"""
A module containing the script
to create the tables in the db
with the correct PK and FK
assignments.

Also manages db connection and 
fetches the password credential
from AWS.
"""
import psycopg2
import boto3
from sqlalchemy import create_engine

#Fetch password
def fetch_password():
    ssm = boto3.client('ssm')
    parameter = ssm.get_parameter(
        Name='redshift-cluster-master-pass', WithDecryption=True)
    password = parameter['Parameter']['Value']

    return password

# postgreSQL connection for creating tables + queries to populate tables with FKs
def fetch_conn():
    mypassword = fetch_password()
    
    conn = psycopg2.connect(
        dbname="dev_delon6_team3",
        host="redshiftcluster-8pp4d8ute2ly.cfahydnz3hic.eu-west-1.redshift.amazonaws.com",
        port="5439",
        user="awsuser",
        password=mypassword
    )

    return conn

#sqlalchemy connection from engine object (for loading dfs)
def fetch_eng_conn():
    mypassword = fetch_password()

    conn_string = f"postgresql://awsuser:{mypassword}@redshiftcluster-8pp4d8ute2ly.cfahydnz3hic.eu-west-1.redshift.amazonaws.com:5439/dev_delon6_team3"
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
            branch_id int IDENTITY NOT NULL,
            branch_name VARCHAR(100) NOT NULL,
            PRIMARY KEY(branch_id));
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
            cust_id INT IDENTITY NOT NULL,
            cust_name VARCHAR(100) NOT NULL,
            cust_card VARCHAR(250),
            PRIMARY KEY(cust_id)
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
            product_id INT IDENTITY NOT NULL,
            product_name VARCHAR(100) NOT NULL,
            product_flavour VARCHAR(100) NOT NULL,
            product_price FLOAT NOT NULL,
            PRIMARY KEY(product_id)
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
            order_id INT IDENTITY NOT NULL,
            time_stamp VARCHAR(100) NOT NULL,
            branch_id INT NOT NULL,
            cust_id INT NOT NULL,
            payment_type VARCHAR(100) NOT NULL,
            total_price FLOAT NOT NULL,
            PRIMARY KEY(order_id),
            FOREIGN KEY(branch_id) REFERENCES branches(branch_id),
            FOREIGN KEY(cust_id) REFERENCES customers(cust_id)
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
            FOREIGN KEY(order_id) REFERENCES orders(order_id),
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        );
        """

    cursor.execute(sql)
    conn.commit()
    conn.close()

# CREATE TABLES
def create_all_tables():
    create_branch_table()
    create_customer_table()
    create_products_table()
    create_orders_table()
    create_basket_table()
