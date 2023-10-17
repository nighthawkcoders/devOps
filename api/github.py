from datetime import datetime, timedelta
import json
import requests
import os
from flask import Blueprint, jsonify  # jsonify creates an endpoint response object
from flask_restful import Api, Resource # used for REST API building
from model.users import *

def get_fragment():
    ten_days_before_now = (datetime.utcnow() - timedelta(days=10)).strftime('%Y-%m-%dT%H:%M:%SZ')

    return f'''
        fragment userInfo on User {{
          login
          contributionsCollection(from: "{ten_days_before_now}") {{
            totalCommitContributions
          }}
        }}
    '''

def generate_github_graphql_query(usernames):
    individual_queries = [
        f'''
            user{i}: user(login: "{username}") {{
              ...userInfo
            }}
        '''
        for i, username in enumerate(usernames)
    ]
    
    full_query = f'''
        {get_fragment()}
        query {{
            {''.join(individual_queries)}
        }}
    '''
    
    return full_query

def send_github_graphql_request(query, api_token):
    headers = {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }
    payload = json.dumps({"query": query})
    response = requests.post('https://api.github.com/graphql', headers=headers, data=payload)
    return response.json()

def parse_graphql_response(response):
    username_to_commits = {
      user_data["login"]: user_data["contributionsCollection"]["totalCommitContributions"]
      for user_data in response["data"].values() if user_data is not None
    }
    return username_to_commits

def get_stats(usernames):
    api_token = os.environ["GITHUB_TOKEN"]

    query = generate_github_graphql_query(usernames)
    response = send_github_graphql_request(query, api_token)
    stats = parse_graphql_response(response)

    return stats

github_api = Blueprint('github_api', __name__,
                   url_prefix='/api/github')

api = Api(github_api)

class GithubAPI:        
    class _Read(Resource):
        def get(self):
            users = User.query.all()
            users_map = { user.uid : user for user in users }
            stats = get_stats(users_map.keys())

            for username, count in stats.items():
                users_map[username].latest_commits = count
                users_map[username].update()

    
    # building RESTapi resources/interfaces, these routes are added to Web Server
    api.add_resource(_Read, '/')


if __name__ == '__main__':
    usernames = ['safinsingh', 'rjawesome', 'vardaansinha']
    
    print(get_stats(usernames))