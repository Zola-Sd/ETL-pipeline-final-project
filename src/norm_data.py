import pandas as pd
from pathlib import Path
import hashlib


def fetch_filepath(filename):
    return Path(__file__).parent/filename


df = pd.read_csv(fetch_filepath('test.csv'))

# print(df)


def store_table():

    df_store_column = df['store'].unique()

    df_table = pd.DataFrame(df_store_column, columns=['Store name'])
    df_table['Store code'] = [store_name[:3].upper()
                              for store_name in df_table['Store name']]

    print(df_store_column)
    print(df_table)


store_table()


def items_table():
    # df_items: item_names, flavour, item_name, combined_id, price
    orders = [order.split(" , ") for order in df['basket_items']]
    # print(orders)
    item_names = []
    prices = []
    print(orders[0])
    for item in orders:
        for value in item:
            item_names.append(value.split("-")[0])
            prices.append(value.split(",")[0])
        prices1 = []
        for val in prices:
            prices1.append(val.split("-")[-1])
        print(prices1[0])

    print(item_names[0])
    print(prices)
    items_dict = {
        'item_names': item_names,
        'prices': prices1
    }

    print(item_names[0])
    print(prices[0])
    print(item_names)
    df_itemd = pd.DataFrame(items_dict, columns=[
                            'item_names', 'prices'])

    print(df_itemd)

    uni_time = df_itemd['item_names'].unique()
    uni_price = df_itemd['prices'].unique()

    print(uni_time)
    print(uni_price)

    df_product_name = pd.DataFrame(uni_time, columns=['Item_names'])
    df_product_name = pd  .DataFrame(uni_price, columns=['price'])

    print(df_product_name)

    # ,'flavour', 'item_name...)
    # df_items = pd.DataFrame(item_names, columns=['item_names'])
    # print(df_items)

    # for item in orders[0]:
    #     print(item.split(" "))


# items_table()
# def format_timestamp():
#     df['timestamp'] = pd.Timestamp('timestamp', format='%d/%m/%Y %H:%M')

#     print(df)


# format_timestamp()


# df['timestamp'] = pd.Timestamp(df['timestamp'])

# print(df.to_string())


def Items_table_test():
    # df_items: item_names, flavour, item_name, combined_id, price
    orders = [order.split(" , ") for order in df['basket_items']]
    # print(orders)
    item_names = []
    prices = []
    # print(orders[0])
    for item in orders:
        for value in item:
            item_names.append(value.split("-")[0])
            prices.append(value.split(",")[0])
            prices1 = []
        for val in prices:
            prices1.append(val.split("-")[-1])
        # print(prices1[0])
    # print(item_names[0])

    # print(item_names)
    # print(prices1)
    #uni_time = list(set(item_names))
    # print(uni_time)
    dict = {"Item_name": item_names,
            "price": prices1, }
    # "index": len(uni_time)}
    df_itemd = pd.DataFrame(dict)
    # trying to add auto incremet id
    #df_itemd.insert(0, 'Item_id', range(0, 0 + len(df_itemd)))
    # print(df_itemd)

    df_dupsremoved = df_itemd.drop_duplicates()

    # print(df_dupsremoved)
    # removes duplicates
    df_dupsremoved_only_name = df_itemd.drop_duplicates(subset=['Item_name'])
    # print(df_dupsremoved_only_name)
    # removes random index
    df_index = df_dupsremoved_only_name.reset_index(drop=True)
    print(df_index)

    # uni_time = df_itemd['Item_name'].unique()

    # # print(uni_time)

    # df_product_name = pd.DataFrame(uni_time, columns=['Item_names'])

    # print(df_product_name)


Items_table_test()


def Trans_table():
    df_trans_time = df['timestamp']
    df_trans_bcode = df['store']
    df_trans_payment = df['cash_or_card']
    df_trans_cust = df['customer_name']
    df_trans_tt = df['total_price']

    print(df_trans_time)
    DictT = {"time_stamp": df_trans_time,
             "store": df_trans_bcode,
             "payment_type": df_trans_payment,
             "Cust_name": df_trans_cust,
             "Total_price": df_trans_tt}

    df_transtable = pd.DataFrame(DictT)
    # checking for duplicates
    df_transtable_no_dups = df_transtable.drop_duplicates(
        subset=['Cust_name'])
    # df_transtable['Time_stamp'] = df_trans_time

    # df_transtable['Payment_type'] = df_trans_payment
    # df_transtable['Cust'] = df_trans_cust
    # df_transtable['Total_price'] = df_trans_tt

    print(df_transtable)
    print(df_transtable_no_dups)


Trans_table()


def customer_table():
    
# Convert column to string
    df['customer_name'] = df['customer_name'].astype(str)
# Apply hashing function to the column
    df['customer_name'] = df['customer_name'].apply(
        lambda x: 
            hashlib.sha256(x.encode()).hexdigest()
)
    df_customer_name_hash=df['customer_name']
    
    df['card_number']=df['card_number'].astype('string')
    df['card_number']=df['card_number'].fillna('CASH')

    df.loc[df['card_number'] =='CASH', 'card_number'] = 'CASH' 
    df.loc[df['card_number'] !='CASH', 'card_number'] = df['card_number'].apply(
        lambda x: 
            hashlib.sha256(x.encode()).hexdigest()
)   



 
    df_card_number_hash=df['card_number']
    # print(df)

    dict_ayub = {"customer_name_hash": df_customer_name_hash,
             "card_number_hash": df_card_number_hash,
             }
    
    df_customer = pd.DataFrame(dict_ayub)
    # checking for duplicates
    df_cust_transformed = df_customer.drop_duplicates(subset=['customer_name_hash','card_number_hash'],keep='first')

    print(df_customer)
    print(df_cust_transformed)

   

customer_table()