import psycopg2 as db_connect
host_name="localhost"
db_user="root"
db_password="password"
db_name="postgres"

connection = db_connect.connect(host=host_name,user=db_user,password=db_password,database=db_name)
 
cursor = connection.cursor()

sql= ''' CREATE TABLE IF NOT EXISTS store_table (Branch_Code varchar, Branch_Name varchar);'''

cursor.execute(sql)
connection.commit()
connection.close()