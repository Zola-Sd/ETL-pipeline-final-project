import psycopg2 as db_connect
host_name="localhost"
db_user="root"
db_password="password"
db_name="postgres"

connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name)
cursor = connection.cursor()

def create_store_table():
    sql= \
        """ 
        CREATE TABLE IF NOT EXISTS store_table( 
        branch_code varchar, 
        branch_name varchar
        );
    """

    cursor.execute(sql)
    connection.commit()

def create_transaction_table():
    sql = \
        """
        CREATE TABLE IF NOT EXISTS transactions_table(
        tran_id INT PRIMARY KEY,
        time varchar, 
        branch_code varchar,
        cust_id int, 
        payment_method varchar,
        total_price float
        );
    """

    cursor.execute(sql)
    connection.commit()

















#func_1()
#func_2()
create_store_table()
create_transaction_table()
connection.close()