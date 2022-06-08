import pandas as pd
from pathlib import Path


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


# store_table()

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

    # print(df_product_name)

    # ,'flavour', 'item_name...)
    # df_items = pd.DataFrame(item_names, columns=['item_names'])
    # print(df_items)

    # for item in orders[0]:
    #     print(item.split(" "))


items_table()
# def format_timestamp():
#     df['timestamp'] = pd.Timestamp('timestamp', format='%d/%m/%Y %H:%M')

#     print(df)


# format_timestamp()


# df['timestamp'] = pd.Timestamp(df['timestamp'])

# print(df.to_string())


def second_col():
    # df_items: item_names, flavour, item_name, combined_id, price
    orders = [order.split(" , ") for order in df['basket_items']]
    # print(orders)
    item_names = []
    print(orders[0])
    for item in orders:
        for value in item:
            item_names.append(value.split("-")[0])
    print(item_names[0])

    print(item_names)
    df_itemd = pd.DataFrame(item_names, columns=['Item_name'])

    uni_time = df_itemd['Item_name'].unique()

    # print(uni_time)

    df_product_name = pd.DataFrame(uni_time, columns=['Item_names'])

    print(df_product_name)
