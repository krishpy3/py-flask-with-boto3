from flask import Flask, render_template, request
import boto3
from pprint import pprint
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
        if request.form['user'] == 'admin' and request.form['pass'] == 'pass':
            msg = 'Login successful'
        else:
            msg = 'Username/Password is not matching'

        return render_template('login.html', message=msg)


app.run(debug=True, port=5000)
