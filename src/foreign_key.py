import psycopg2 as db_connect
host_name = "localhost"
db_user = "root"
db_password = "password"
db_name = "postgres"

# Establishing DB connection
connection = db_connect.connect(
    host=host_name, user=db_user, password=db_password, database=db_name)
cursor = connection.cursor()

# Alter transaction table to Add Foreign keys


def alter_tran_table():
    sql = \
        '''
        ALTER TABLE transactions_table
        ADD FOREIGN KEY (cust_id) REFERENCES cust_table(cust_id),
        ADD FOREIGN KEY (branch_id) REFERENCES store_table(branch_id),
        ADD FOREIGN KEY (order_id) REFERENCES basket_table(order_id);
        '''

    cursor.execute(sql)
    connection.commit()

# Alter basket table to add foreign keys


def alter_basket_table():
    sql = \
        '''
        ALTER TABLE basket_table
        ADD FOREIGN KEY (cust_id) REFERENCES cust_table(cust_id),
        ADD FOREIGN KEY (item_id) REFERENCES items_table(item_id);
        '''
# Execut SQL Code
    cursor.execute(sql)
    connection.commit()


# Running functions
alter_tran_table()
alter_basket_table()

# Closing DB connection
connection.close()
