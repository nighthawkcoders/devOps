from datetime import datetime, timedelta
import json
import requests
import os

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
      for user_data in response["data"].values()
    }
    return username_to_commits

usernames = ['safinsingh', 'rjawesome', 'vardaansinha']
api_token = os.environ["GITHUB_TOKEN"]

query = generate_github_graphql_query(usernames)
response = send_github_graphql_request(query, api_token)
stats = parse_graphql_response(response)

print(stats)