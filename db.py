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


def get_user(user_id: str):
    user = users_table.get_item(Key={'user_id': user_id}).get('Item')
    return user


def get_user_by_username(username: str):
    results = users_table.query(
        IndexName='usernameIndex',
        KeyConditionExpression=Key('username').eq(username)
    ).get('Items')
    if results:
        user = results[0]
        return user


def create_user(user_id: str, username: str, email: str, name: str, bio: str, location: str, joined_at: str,
                hashed_password: str, superuser: bool):
    user = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'name': name,
        'bio': bio,
        'location': location,
        'joined_at': joined_at,
        'hashed_password': hashed_password,
        'superuser': superuser
    }
    try:
        users_table.put_item(
            Item=user,
            ConditionExpression='attribute_not_exists(user_id) and attribute_not_exists(username)',
        )
    except db.meta.client.exceptions.ConditionalCheckFailedException:
        return
    else:
        return user


def update_user(user_id: str, username: str, email: str, name: str, bio: str, location: str, hashed_password: str,
                superuser: bool):
    try:
        response = users_table.update_item(
            Key={
                'user_id': user_id
            },
            ConditionExpression='attribute_exists(user_id)',
            UpdateExpression='set username=:username, email=:email, #name=:name, bio=:bio, #location=:location, '
                             'hashed_password=:hashed_password, superuser=:superuser',
            ExpressionAttributeNames={
                '#name': 'name',
                '#location': 'location'
            },
            ExpressionAttributeValues={
                ':username': username,
                ':email': email,
                ':name': name,
                ':bio': bio,
                ':location': location,
                ':hashed_password': hashed_password,
                ':superuser': superuser
            },
            ReturnValues='ALL_NEW'
        )
    except db.meta.client.exceptions.ConditionalCheckFailedException:
        return
    else:
        return response['Attributes']
