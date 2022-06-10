import psycopg2 as db_connect
host_name = "localhost"
db_user = "root"
db_password = "password"
db_name = "postgres"

connection = db_connect.connect(
    host=host_name, user=db_user, password=db_password, database=db_name)
cursor = connection.cursor()


def alter_tran_table():
    sql = \
        '''
        ALTER TABLE transactions_table
        ADD FOREIGN KEY (cust_id) REFERENCES transactions_table(trans_id),
        ADD FOREIGN KEY (branch_id) REFERENCES transactions_table(trans_id);
        '''

    cursor.execute(sql)
    connection.commit()


def alter_basket_table():
    sql = \
        '''
        ALTER TABLE basket_table
        ADD FOREIGN KEY (cust_id) REFERENCES basket_table(order_id),
        ADD FOREIGN KEY (item_id) REFERENCES basket_table(order_id);
        
        '''

    cursor.execute(sql)
    connection.commit()


alter_tran_table()
alter_basket_table()
connection.close()
