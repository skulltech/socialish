import os

import boto3
from boto3.dynamodb.conditions import Key

USERS_TABLE = os.environ['USERS_TABLE']
POSTS_TABLE = os.environ['POSTS_TABLE']
COMMENTS_TABLE = os.environ['COMMENTS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    db = boto3.resource(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    db = boto3.resource('dynamodb')
users_table = db.Table(USERS_TABLE)
posts_table = db.Table(POSTS_TABLE)
comments_table = db.Table(COMMENTS_TABLE)


def get_user(id: str):
    user = users_table.get_item(Key={'id': id}).get('Item')
    return user


def get_user_by_username(username: str):
    results = users_table.query(
        IndexName='usernameIndex',
        KeyConditionExpression=Key('username').eq(username)
    ).get('Items')
    if results:
        user = results[0]
        return user
