import norm_data as n
import sql_script as ss

#Create connection and cursor objects
connection = ss.fetch_connection()
cursor = connection.cursor()

#Store dfs 
store_df = n.store_table()
items_df = n.items_table()
cust_df = n.customer_table()
trans_df = n.Trans_table()

def load_stores(data):
