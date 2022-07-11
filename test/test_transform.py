"""
A module containing some basic
tests for functions in transform.py.
This module needs to be executed with pytest.
"""
import pandas as pd
import sys
sys.path.append("..")
import src.transform as tr

def test_create_branches_df():
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

def test_hash_value_when_value_is_not_nan():
    #Arrange
    x = 'hash me'

    expected = 'eb201af5aaf0d60629d3d2a61e466cfc0fedb517add831ecac5235e1daa963d6'

    #Act
    actual = tr.hash_value(x)

    #Assert
    assert actual == expected

def test_hash_value_when_value_is_nan():
    #Arrange
    x = 'nan'

    expected = x

    #Act
    actual = tr.hash_value(x)

    #Assert
    assert actual == expected

def test_create_customer_df():
    #Arrange
    cust_dict = {
        'cust_name': ['Cameron Tee', 'Please work', 'Jakub please save us'],
        'cust_card': [3849485923093478, 'nan', '3478409512896587']
    }
    df = pd.DataFrame(cust_dict)
    
    #Expected hashed values from cust_dict
    expected_dict = {
        'cust_name': [
        '4646fa054cfee55350ff9b15431ca38e0f070be1b76aa4b09bd6af98dc3a4388', 
        '3e98b7b69771c90209193bed1f3b369b727c3f5c2ef2645064787d47db6b91c1', 
        '95ff3ee7757e04aeecb2a57202e3de9b1bc8f7464a3808b09ad00f9f3438918e'
        ],
        'cust_card': [
        '5a0fd829e131bacaf038d3777d418779dfdcc5bfd77d1fc8e0f23c85eec97742', 
        'nan', 
        '846a92e61ee8ad953f0fad4af8a9f038fcde9447537023a796e1f23318c42f4c'
        ]
    }
    expected_df = pd.DataFrame(expected_dict)   
    
    expected = expected_df

    #Act
    actual = tr.create_customer_df(df)

    #Assert
    pd.testing.assert_frame_equal(expected, actual)

def test_fetch_products():
    #Arrange
    products_df = pd.DataFrame({'basket_items': ['Regular Glass of milk - 0.70, Regular Smoothies - Glowing Greens - 2.00']})

    expected_data = {'basket_items': [['Regular Glass of milk - 0.70', 'Regular Smoothies - Glowing Greens - 2.00']]}

    expected = pd.DataFrame(expected_data)

    #Act
    actual = tr.fetch_products(products_df)

    #Assert
    pd.testing.assert_frame_equal(expected, actual)

def test_create_products_df():
    #Arrange
    products_df = pd.DataFrame({
                    'basket_items': [
                        'Regular Glass of milk - 0.70', 
                        'Regular Glass of milk - 0.70',
                        'Regular Smoothies - Glowing Greens - 2.00'
                        ]
                    }
                )

    expected_data = {
        'product_name': ['Regular Glass of milk', 'Regular Smoothies'],
        'product_flavour': ['Original', 'Glowing Greens'],
        'product_price': ['0.70', '2.00']
    }
    expected = pd.DataFrame(expected_data)
    
    #Act
    actual = tr.create_products_df(products_df)

    #Assert
    pd.testing.assert_frame_equal(expected, actual)

