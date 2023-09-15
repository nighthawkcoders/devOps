# import "packages" from flask
from flask import render_template, Response
import requests  # import render_template from "public" flask libraries
import boto3
import os
import json
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

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


# setup App pages
from projects.projects import app_projects # Blueprint directory import projects definition

# Initialize the SQLAlchemy object to work with the Flask app instance
db.init_app(app)

# register URIs
app.register_blueprint(joke_api) # register api routes
app.register_blueprint(covid_api) # register api routes
app.register_blueprint(user_api) # register api routes
app.register_blueprint(player_api)
app.register_blueprint(app_projects) # register app pages
load_dotenv()  # Load environment variables from .env file

AWS_ACCESS_KEY = os.environ.get("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.environ.get("AWS_SECRET_KEY")


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
        users_per_server[server] = [user["username"] for user in users]

    return render_template('assignments.html', users_per_server=users_per_server)

@app.route('/create_users')
def create_users():
    users = User.query.all()
    iam = boto3.client(
        "iam",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
    )

    for user in users:
        print(user.uid)

        try:
            # check if the user alread exists
            iam.get_user(UserName=user.uid)
        except iam.exceptions.NoSuchEntityException:
            iam.create_user(UserName=user.uid)
            iam.add_user_to_group(UserName=user, GroupName="Student")

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
