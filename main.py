# import "packages" from flask
from flask import render_template, Response, redirect, url_for, request
import requests  # import render_template from "public" flask libraries
import boto3
import botocore
import os
import json
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import unquote
from datetime import datetime
import pytz
# import "packages" from "this" project
from __init__ import app,db  # Definitions initialization
from model.jokes import initJokes
from model.users import User, initUsers
from model.players import initPlayers


# setup APIs
from api.covid import covid_api # Blueprint import api definition
from api.joke import joke_api # Blueprint import api definition
from api.user import user_api # Blueprint import api definition
from api.player import player_api
from api.github import github_api


# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition

import time

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# register URIs
app.register_blueprint(joke_api) # register api routes
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects) # register app pages
app.register_blueprint(github_api)
load_dotenv()  # Load environment variables from .env file

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")


try:
    with open('./kasm.json') as f:
        KASM_SERVERS = json.load(f)
except:
    # file doesnt exist/malformed
    KASM_SERVERS = {}
    print("Kasm Servers not avaliable")


def get_users(api_key, api_key_secret, api_base_url):
    endpoint = f"{api_base_url}/api/public/get_users"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "api_key": api_key,
        "api_key_secret": api_key_secret
    }
    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code != 200:
        print(f"Error getting users from {api_base_url}")
        return []

    users_list = response.json().get("users", [])
    filtered_users = [user for user in users_list if "@kasm.local" not in user.get("username")]
    return filtered_users

def get_user_mappings():
    mappings = {}
    for server, server_info in KASM_SERVERS.items():
        endpoint = f"{server}/api/public/get_users"
        headers = {
            "Content-Type": "application/json"
        }
        payload = {
            "api_key": server_info["api_key"],
            "api_key_secret": server_info["api_key_secret"]
        }
        response = requests.post(endpoint, json=payload, headers=headers)

        users_list = response.json().get("users", [])
        filtered_users = [user.get("username") for user in users_list if "@kasm.local" not in user.get("username")]
        mappings[server] = filtered_users
    return mappings

@app.errorhandler(404)  # catch for URL not found
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route('/')  # connects default URL to index() function
def index():
    return render_template("index.html")

@app.route('/table/')  # connects /stub/ URL to stub() function
def table():
    return render_template("table.html")

@app.route('/users/')
def users():
    table = User.query.all()
    return render_template("users.html", table=table)

@app.route('/update_users_kasm')
def update_kasm():
    mappings = get_user_mappings()
    for server, users in mappings.items():
        for u in users:
            db_user = User.query.filter(User._uid.ilike(u)).first()
            if db_user != None:
                db_user.kasm_server = server
                db_user.update()
    return "Update Completed"

@app.route('/server_users.csv')
def server_users():
    table = User.query.filter_by(_server_needed=True)
    csv_str = "uid, first_name,last_name"
    for user in table:
        first = user.first_name[0] if isinstance(user.first_name, list) else user.first_name
        csv_str += "\n" + user.uid + ","+ first + "," + user.last_name
    return Response(csv_str, mimetype='text/csv')


@app.route('/assignments')
def assignments():
    users_per_server = {}
    for server, server_info in KASM_SERVERS.items():
        api_key = server_info["api_key"]
        api_key_secret = server_info["api_key_secret"]
        users = get_users(api_key, api_key_secret, server)
        server = server.replace("https://", "")
        for user in users:
            if "last_session" in user and user["last_session"]:
                utc_timestamp = user["last_session"]
                try:
                    utc_timestamp = datetime.strptime(utc_timestamp, "%Y-%m-%d %H:%M:%S.%f")
                    utc_timestamp = pytz.utc.localize(utc_timestamp)
                    pst_timezone = pytz.timezone('America/Los_Angeles')
                    pst_timestamp = utc_timestamp.astimezone(pst_timezone)
                    user["last_session"] = pst_timestamp.strftime("%Y-%m-%d %H:%M:%S")
                except ValueError:
                    # Handle invalid timestamp format here
                    user["last_session"] = "No Timestamp Found"

        users_per_server[server] = users
    return render_template('assignments.html', users_per_server=users_per_server)



@app.route('/delete/<server>/<username>', methods=['POST'])
def delete_user(server, username):
    print(server)
    print(username)
    password = request.form.get('password')
    if password != ADMIN_PASSWORD:
        return redirect(url_for('assignments'))
    # add https to server if not there
    server = "https://" + server
    if server in KASM_SERVERS:
        api_key = KASM_SERVERS[server]["api_key"]
        api_key_secret = KASM_SERVERS[server]["api_key_secret"]
        api_base_url = server

        # Get the user_id based on the username
        user_id = get_user_id(api_key, api_key_secret, api_base_url, username)
        print(user_id)
        if user_id:
            # Construct the API endpoint for user deletion
            endpoint = f"{api_base_url}/api/public/delete_user"

            # Construct the payload with API key, API key secret, and target user_id
            payload = {
                "api_key": api_key,
                "api_key_secret": api_key_secret,
                "target_user": {
                    "user_id": user_id
                },
                "force": True  # You can change this as needed
            }

            # Send a DELETE request to the Kasm API
            response = requests.post(endpoint, json=payload)

            # Check the response and handle any errors
            if response.status_code == 200:
                # User deleted successfully, handle success
                print(f"User {username} deleted successfully!", 'success')
            else:
                # Handle error cases, e.g., API error
                print(f"Error deleting user {username}: {response.text}", 'error')
        else:
            # Handle the case where user_id is not found
            print(f"User {username} not found in {server}", 'error')

    return redirect(url_for('assignments'))

def get_user_id(api_key, api_key_secret, api_base_url, username):
    endpoint = f"{api_base_url}/api/public/get_users"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "api_key": api_key,
        "api_key_secret": api_key_secret
    }

    response = requests.post(endpoint, json=payload, headers=headers)

    if response.status_code == 200:
        users = response.json().get("users", [])
        for user in users:
            if user.get("username") == username:
                return user.get("user_id")

    return None

@app.route('/create_users')
def create_users():
    users = User.query.all()
    iam = boto3.client(
        "iam",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )

    for user in users:
        try:
            # check if the user already exists
            iam.get_user(UserName=user.uid)
        except iam.exceptions.NoSuchEntityException:
            iam.create_user(UserName=user.uid)
            time.sleep(.100)
            iam.add_user_to_group(UserName=user.uid, GroupName="Student")
            time.sleep(.100)
            iam.create_login_profile(UserName=user.uid, Password="123Qwerty!", PasswordResetRequired=True)
        except botocore.exceptions.ClientError as e:
            print("Error with the following user")
            print(user.uid)
            print(e)

    return "Completed"

def get_instances(region_name):
    ec2_client = boto3.client(
        "ec2",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=region_name
    )

    response = ec2_client.describe_instances(Filters=[{"Name": "tag:Name", "Values": ["Kasm*"]}])

    instances = []
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            domain_tag = next((tag for tag in instance["Tags"] if tag["Key"] == "Domain"), None)
            domain = domain_tag["Value"] if domain_tag else "Unknown Domain"

            instances.append({
                "Region": region_name,
                "InstanceId": instance["InstanceId"],
                "DisplayName": domain,
                "State": instance["State"]["Name"],
            })

    return instances

@app.route("/servers")
def servers():
    regions = boto3.client("ec2").describe_regions()["Regions"]

    instances = []
    with ThreadPoolExecutor() as executor:
        for region in regions:
            region_name = region["RegionName"]
            instances.extend(executor.submit(get_instances, region_name).result())

    return render_template("servers.html", instances=instances)


@app.before_first_request
def activate_job():  # activate these items
    initJokes()
    initUsers()
    initPlayers()

# this runs the application on the development server
if __name__ == "__main__":
    # change name for testing
    from flask_cors import CORS
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.run(debug=True, host="0.0.0.0", port="8180")
