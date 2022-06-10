import psycopg2 as db_connect
host_name = "localhost"
db_user = "root"
db_password = "password"
db_name = "postgres"

# Establishing DB connection

connection = db_connect.connect(
    host=host_name, user=db_user, password=db_password, database=db_name)
cursor = connection.cursor()

# Creating store table


def create_store_table():
    sql = \
        """ 
        CREATE TABLE IF NOT EXISTS store_table( 
        branch_id SERIAL PRIMARY KEY,
        branch_code varchar, 
        branch_name varchar
        );
    """

    cursor.execute(sql)
    connection.commit()

# Creating transaction table


def create_transaction_table():
    sql = \
        """
        CREATE TABLE IF NOT EXISTS transactions_table(
        trans_id SERIAL PRIMARY KEY,
        order_id int,
        time varchar, 
        branch_id int,
        cust_id int, 
        payment_method varchar,
        total_price float
        );
    """

    cursor.execute(sql)
    connection.commit()

# Creating items table


def create_items_table():
    sql = \
        """
        CREATE TABLE IF NOT EXISTS items_table(
        item_id SERIAL PRIMARY KEY,
        item_name varchar, 
        item_price float
        );
    """

    cursor.execute(sql)
    connection.commit()


# Creating customer table
def customer_table():
    sql = \
        ''' 
        CREATE TABLE IF NOT EXISTS cust_table(
            cust_id SERIAL PRIMARY KEY, 
            cust_name VARCHAR,
            cust_card int
            
            );'''

    cursor.execute(sql)
    connection.commit()

# Creating basket table


def create_basket_table():
    sql = \
        """
        CREATE TABLE IF NOT EXISTS basket_table(
            order_id SERIAL PRIMARY KEY,
            cust_id int,
            item_id int,
            total_price float
            );
    """
    cursor.execute(sql)
    connection.commit()


# Running functions
create_store_table()
create_transaction_table()
create_items_table()
create_basket_table()
customer_table()
# Closing DB connection
connection.close()
