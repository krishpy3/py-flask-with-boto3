from flask import Flask, render_template, request, jsonify
import boto3
from pprint import pprint
import sqlite3

conn = sqlite3.connect('test.sqlite3', check_same_thread=False)
cur = conn.cursor()

app = Flask(__name__)

session = boto3.Session(profile_name='default')


@app.route('/')
def display_names():
    name = 'Krish'
    services = ['s3', 'ec2', 'iam.users']
    return render_template('base.html')


@app.route('/s3')
def s3():
    s3 = session.client('s3')
    res = s3.list_buckets()
    buc_dict = {}
    for bucket in res['Buckets']:
        obj_list = []
        objs = s3.list_objects(Bucket=bucket['Name'])
        for obj in objs.get('Contents', []):
            obj_list.append(obj['Key'])
        buc_dict[bucket['Name']] = obj_list
    pprint(buc_dict)
    return render_template('s3.html', res=buc_dict)


@app.route('/ec2')
def ec2():
    ec2 = session.client('ec2')
    ec2_regions = ec2.describe_regions()
    return render_template('ec2.html', regions=ec2_regions)


@app.route('/ec2/<region>')
def ec2_region(region):
    ec2 = session.client('ec2', region_name=region)
    res = ec2.describe_instances()
    return render_template('ec2_region.html', res=res)


@app.route('/about-us')
def about():
    return 'Its me..!'


@app.route('/contact-us')
def contact():
    return 'Catch us if you can..!'


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    elif request.method == 'POST':
        cur.execute("SELECT username,password FROM user WHERE username = '{}'".format(
            request.form['user']))
        database_output = cur.fetchone()
        if database_output != None:
            if database_output[1] == request.form['pass']:
                msg = 'Login successful'
            else:
                msg = 'Password is not matching'
        elif database_output == None:
            msg = 'Username not available'
        # if request.form['user'] == 'admin' and request.form['pass'] == 'pass':
        # else:

        return render_template('login.html', message=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    elif request.method == 'POST':
        if request.form['password'] == request.form['re_password']:
            data_add = (request.form['username'], request.form['first_name'],
                        request.form['last_name'], request.form['password'])
            cur.execute("""INSERT INTO user
                (username,first_name,last_name,password) VALUES {}""".format(data_add))
            conn.commit()
            return render_template('register.html', success="User added")

        else:
            error = 'Password not matching'
            return render_template('register.html', error=error)


def check_user(client, userName):
    try:
        res = client.get_user(UserName=userName)
        return res['User']
    except:
        return {'error': 'User not available'}

# /api/iam/ -> get method


def list_users():
    iam = session.client('iam')
    pages = iam.get_paginator('list_users')
    total_data = []
    for page in pages.paginate():
        total_data.extend(page['Users'])
    return total_data

# /api/iam/ -> POST method


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


def get_user(userName):
    iam = session.client('iam')
    output = check_user(iam, userName)
    return output


def update_user(userName, newName):
    iam = session.client('iam')
    output = check_user(iam, userName)
    if 'error' in output:
        return output
    else:
        res = iam.update_user(
            UserName=userName,
            NewUserName=newName
        )
        return {'message': 'User Updated'}


def delete_user(userName):
    iam = session.client('iam')
    output = check_user(iam, userName)
    if 'error' in output:
        return output
    else:
        res = iam.delete_user(
            UserName=userName,
        )
        return {'message': 'User deleted'}


@app.route('/api/iam/', methods=['GET', "POST"])
def iam_list_view():
    if request.method == 'GET':
        return jsonify(list_users())
    elif request.method == 'POST':
        return jsonify(create_user(request.form['username']))


@app.route('/api/iam/<username>', methods=['GET', 'PUT', 'DELETE'])
def iam_detail_view(username):
    if request.method == 'GET':
        return get_user(username)
    elif request.method == 'PUT':
        return update_user(username, request.form['username'])
    elif request.method == 'DELETE':
        return delete_user(username)


@app.route('/iam/')
def iam_db():
    cur.execute('SELECT COUNT(*) FROM iam_user')
    total_user = cur.fetchone()[0]
    query = 'SELECT * FROM iam_user'
    user_per_page = 10
    if request.args.get('family'):
        query += f" WHERE family = '{request.args['family']}'"
    if request.args.get('page'):
        page = int(request.args.get('page'))
        offset = page*user_per_page
    else:
        page = 1
        offset = 0
    query += f' Limit {user_per_page} OFFSET {offset}'
    print(query)
    cur.execute(query)
    user_list = cur.fetchall()
    total_page = total_user // user_per_page + 1
    if page < total_page:
        next_page = True
        next_value = page + 1

        previous = True
        previous_value = page - 1

    return render_template('iam.html', user_list=user_list)


app.run(debug=True, port=5000)
