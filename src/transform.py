"""
A module handling the transformations
on the raw data csv(s).
Each function will return a dataframe
to be loaded into the respective tables
in the db.
"""
import pandas as pd
import hashlib
import db_manager as dbm
import boto3

def create_branches_df(df):
    """
    - Returns a df with the unique branch_names
    """
    branches_df = pd.DataFrame(df['branch_name'].unique(), columns=['branch_name'])

    return branches_df

def hash_value(x):
    """
    - Hashes x with hashlib.sha256
    """
    if x != 'nan':
        return hashlib.sha256(x.encode()).hexdigest()
    else:
        return x

def create_customer_df(df):
    """
    - Returns a df with the unique customers
    - PII so values are hashed
    """
    #TODO: fix 'nan' values. Set them to NULL in the db

    #Create unhashed df containing names and card numbers
    unhashed_cust_df = df[['cust_name', 'cust_card']]

    #Convert whole df to string
    unhashed_cust_df = unhashed_cust_df.astype(str)

    #Remove duplicates - default subset arg. is whole df, default keep arg. is first
    unhashed_cust_df = unhashed_cust_df.drop_duplicates()
   
    #Hash values if they are not 'nan', else return 'nan'
    hashed_cust_df = unhashed_cust_df.applymap(lambda x: hash_value(x))

    return hashed_cust_df

def fetch_products(df):
    """
    - Returns a df with all products and details in the raw data
    - Must be transformed
    """
    #Split the basket_items col so that each row is a list
    items_series = df['basket_items'].apply(lambda x: x.split(", "))
    
    #Load this pd.Series object into a pd.DataFrame. Unwanted column - dropped after transformation
    products_df = pd.DataFrame(items_series, columns=['basket_items'])

    #Query for max order_id to be the starting order_id of the new data getting loaded in
    conn = dbm.fetch_conn()
    cursor = conn.cursor()

    sql = \
        """
        SELECT MAX(order_id) 
        FROM orders;
        """

    cursor.execute(sql)
    response = cursor.fetchone()
    print(response)
    max_order_id = response[0]
    print(max_order_id)
    
    if max_order_id != None:
        starting_order_id = max_order_id + 1

        order_ids = [order_id for order_id in range(starting_order_id, starting_order_id + len(products_df.index))]

        products_df['order_id'] = order_ids
    else:
        products_df['order_id'] = products_df.index + 1

    #Explode contents of each order so that every item in an order is a separate row in the df
    products_df = products_df.explode('basket_items')
    
    return products_df

def create_products_df(df):
    """
    - Returns a df which transforms the unique products and details
    """
    products_df = fetch_products(df)

    #Drop order_id column - not required for product table transformation
    products_df = products_df.drop(columns=['order_id'])

    #Get unique products
    products_df = products_df.drop_duplicates(ignore_index=True)
    
    product_names, product_flavours, product_prices = [], [], []

    for product in products_df['basket_items']:
        details = product.split(' - ')
        #Append name and price (always first and last elements of details)
        product_name = f'{details[0]}'
        product_names.append(product_name)

        product_price = f'{details[-1]}'
        product_prices.append(product_price)

        #Handle flavours
        if 'Flavoured' in product:
            #Append flavour
            product_flavour = f'{details[1]}'
            product_flavours.append(product_flavour)
        else:
            #Append 'Original'
            product_no_flavour = f'Original'
            product_flavours.append(product_no_flavour)
        
    #Populate products_df with new columns
    products_df['product_name'] = product_names
    products_df['product_flavour'] = product_flavours
    products_df['product_price'] = product_prices

    #Drop unwanted column
    products_df = products_df.drop(columns=['basket_items'])
    
    return products_df
    
def create_orders_df(df):
    """
    - Returns a df containing orders and the accompanying information
    - branch_id and cust_id columns rely on data which has to be loaded into 
    the db first (for the queries)
    """
    orders_df_without_ids = df[['time_stamp', 'branch_name', 'cust_name', 'payment_type', 'total_price']]

    #Check for duplicates
    orders_df_without_ids = orders_df_without_ids.drop_duplicates()

    #Fetch conn and cursor objects
    conn = dbm.fetch_conn()
    cursor = conn.cursor()

    #Query branch_ids and cust_ids from their tables and populate into orders_df
    branch_vals = [val for val in orders_df_without_ids['branch_name']]
    branch_ids = []
    for branch_val in branch_vals:
        sql = \
            f'''
            SELECT branch_id
            FROM branches
            WHERE branch_name = '{branch_val}'
            '''
        cursor.execute(sql)
        record = cursor.fetchone()
        #Returns a tuple with id at idx = 0
        branch_ids.append(record[0])
    
    cust_vals = [val for val in orders_df_without_ids['cust_name']]
    cust_ids = []
    for cust_val in cust_vals:
        sql = \
            f'''
            SELECT cust_id
            FROM customers
            WHERE cust_name = '{hash_value(cust_val)}'
            '''
        cursor.execute(sql)
        record = cursor.fetchone()
        cust_ids.append(record[0])
    
    conn.close()
    
    #Make new df with the new columns
    orders_df = pd.DataFrame(orders_df_without_ids, columns=['time_stamp', 'branch_id', 'cust_id', 'payment_type', 'total_price'])
    
    #Populate id columns with queried values
    orders_df['branch_id'] = branch_ids
    orders_df['cust_id'] = cust_ids

    return orders_df

def create_basket_df(df):
    """
    - Returns a df containing individual products from each order
    - cols: order_id, product_id
    """
    products_df = fetch_products(df)

    #Names and flavours of all individual products from every order
    product_names = []

    #TODO: refactor this? Repeating code from create_products_df()
    for product in products_df['basket_items']:
        details = product.split(' - ')
        if 'Flavoured' in product:
            product_and_flavour = f'{details[0]} {details[1]}'
            product_names.append(product_and_flavour)
        else:
            product_no_flavour = f'{details[0]} Original'
            product_names.append(product_no_flavour)

    #Query products table to get all the product_names and product_ids
    conn = dbm.fetch_conn()
    cursor = conn.cursor()

    sql = \
        '''
        SELECT product_id, product_name, product_flavour
        FROM products
        '''
    cursor.execute(sql)

    #List of tuples where each tuple is a row in products table
    products = cursor.fetchall()

    #Dict - keys: product_names, values: product_ids (from products table)
    products_dict = {}

    for product in products:
        product_name = f'{product[1]} {product[2]}'
        product_id = str(product[0])
        products_dict[product_name] = product_id

    #Get product_ids from products_dict
    product_ids = [products_dict.get(product_name) for product_name in product_names]

    #Create dict to be loaded into df which is then loaded to db
    basket_dict = {
        'product_id': product_ids,
        'order_id': products_df['order_id']
    }

    basket_df = pd.DataFrame(basket_dict)

    return basket_df

def remove_duplicate_branches():
    conn = dbm.fetch_conn()
    cursor = conn.cursor()

    sql = \
        """
        WITH CTE(branch_id, branch_name, duplicatecount)
        AS (SELECT branch_id, branch_name, ROW_NUMBER() OVER(PARTITION BY branch_name ORDER BY branch_id) AS DuplicateCount
            FROM branches)
        DELETE FROM branches
        USING CTE
        WHERE branches.branch_id = CTE.branch_id
        AND branches.branch_name = CTE.branch_name
        AND duplicatecount > 1;
        """
    
    cursor.execute(sql)
    conn.commit()
    conn.close()

def remove_duplicate_products():
    conn = dbm.fetch_conn()
    cursor = conn.cursor()

    sql = \
        """
        WITH CTE(product_id, product_name, product_flavour, product_price, duplicatecount)
        AS (SELECT product_id, product_name, product_flavour, product_price, ROW_NUMBER() OVER(PARTITION BY product_name, product_flavour, product_price ORDER BY product_id) AS DuplicateCount
            FROM products)
        DELETE FROM products
        USING CTE
        WHERE products.product_id = CTE.product_id
        AND products.product_name = CTE.product_name
        AND duplicatecount > 1;
        """

    cursor.execute(sql)
    conn.commit()
    conn.close()

def remove_duplicate_customers():
    conn = dbm.fetch_conn()
    cursor = conn.cursor()

    sql = \
        """
        WITH CTE(cust_id, cust_name, cust_card, duplicatecount)
        AS (SELECT cust_id, cust_name, cust_card, ROW_NUMBER() OVER(PARTITION BY cust_name, cust_card ORDER BY cust_id) AS DuplicateCount
            FROM customers)
        DELETE FROM customers
        USING CTE
        WHERE customers.cust_id = CTE.cust_id
        AND customers.cust_name = CTE.cust_name
        AND duplicatecount > 1;
        """

    cursor.execute(sql)
    conn.commit()
    conn.close()

