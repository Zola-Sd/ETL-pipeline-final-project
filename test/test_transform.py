import unittest
import pandas as pd
import sys
import hashlib
sys.path.append("..")
import src.transform as tr

class TestTransform(unittest.TestCase):
    def test_create_branches_df(self):
        #Arrange - Mock inputs of the function and expected return value
        df = pd.DataFrame({
            'branch_name': [
                    'Longridge',
                    'Chesterfield',
                    'Uppingham', 
                    'Longridge',
                    'Chesterfield',
                    'Uppingham'
                ]
            }
        )

        expected = pd.DataFrame({'branch_name': ['Longridge', 'Chesterfield', 'Uppingham']})
        
        #Act - invoke the function: create_branches_df
        actual = tr.create_branches_df(df)

        #Assert
        pd.testing.assert_frame_equal(expected, actual)

    def test_hash_value_when_value_is_not_nan(self):
        #Arrange
        x = 'hash me'

        expected = hashlib.sha256(x.encode()).hexdigest()

        #Act
        actual = tr.hash_value(x)

        #Assert
        assert actual == expected

    def test_hash_value_when_value_is_nan(self):
        #Arrange
        x = 'nan'

        expected = x

        #Act
        actual = tr.hash_value(x)

        #Assert
        assert actual == expected

    def test_create_customer_df(self):
        #Arrange
        cust_dict = {
            'cust_name': ['Cameron Tee', 'Please work', 'Jakub please save us'],
            'cust_card': [3849485923093478, 'nan', '3478409512896587']
        }
        df = pd.DataFrame(cust_dict)
        unhashed_df = df.astype(str)
        hashed_df = unhashed_df.applymap(lambda x: tr.hash_value(x))

        expected = hashed_df

        #Act
        actual = tr.create_customer_df(df)

        #Assert
        pd.testing.assert_frame_equal(expected, actual)

    def test_fetch_products(self):
        #Arrange
        products_dict = {
            'basket_items': ['Regular Glass of milk - 0.70, Regular Smoothies - Glowing Greens - 2.00']
        }
        products_df = pd.DataFrame(products_dict)

        products_series = products_df['basket_items'].apply(lambda x: x.split(", "))
        
        expected = pd.DataFrame(products_series)

        #Act
        actual = tr.fetch_products(products_df)

        #Assert
        pd.testing.assert_frame_equal(expected, actual)
        
# unittest.main()
        