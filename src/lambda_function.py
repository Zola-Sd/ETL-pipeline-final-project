import psycopg2
import sqlalchemy
import logging
import boto3
import pandas as pd
from handler import run_app

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print(s3)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    response = s3.get_object(Bucket=bucket, Key=key)
    
    field_names = ['time_stamp', 'branch_name', 'cust_name', 'basket_items', 'total_price', 'payment_type', 'cust_card']
    df = pd.read_csv(response['Body'], names=field_names)
    
    run_app(df)
    
    print("successfully loaded")
