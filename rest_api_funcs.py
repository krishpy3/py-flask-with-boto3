# /iam/   -> get(optional, page-number), post(input needed)
# /iam/id -> get(noinput), put(input needed), delete(noinput)


import boto3
session = boto3.Session(profile_name='default')


def check_user(client, userName):
    try:
        res = client.get_user(UserName=userName)
        return res['Users']
    except:
        return {'error': 'User not available'}


def list_users():
    iam = session.client('iam')
    pages = iam.get_paginator('list_users')
    for page in pages.paginate():
        for user in page['Users']:
            print(user)


list_users()


def get_user(userName):
    iam = session.client('iam')
    output = check_user(iam, userName)
    # if 'error' in output:
    return output


get_user('krish')


def create_user(userName):
    iam = session.client('iam')
    output = check_user(iam, userName)
    if 'error' in output:
        res = iam.create_user(
            UserName=userName
        )
        return res['User']
    else:
        return {'message': 'User is already available'}


def update_user(userName, data):
    iam = session.client('iam')
    output = check_user(iam, userName)
    if 'error' in output:
        return output
    else:
        res = iam.update_user(
            UserName=userName,
            NewUserName=data['newName']
        )
        return res


def delete_user(userName):
    iam = session.client('iam')
    output = check_user(iam, userName)
    if 'error' in output:
        return output
    else:
        res = iam.update_user(
            UserName=userName,
        )
        return {'message': 'User deleted'}
