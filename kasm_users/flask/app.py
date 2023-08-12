from flask import Flask, render_template, redirect, url_for
import requests

app = Flask(__name__)

KASM_SERVERS = {
    "https://kasm100.nighthawkcodingsociety.com": {
        "api_key": "oNca0QZwki2y",
        "api_key_secret": "pgvOIBcmDNZXKq04zdmPltz7ixs9hoYj"
    },
    "https://kasm101.nighthawkcodingsociety.com": {
        "api_key": "nbjIDH6zO5LJ",
        "api_key_secret": "rF4bS7QJUrbttxyzsHAEVT6mYpOor8ty"
    },
    "https://kasm102.nighthawkcodingsociety.com": {
        "api_key": "MUGRY8VuxFf3",
        "api_key_secret": "QRdDGD30myezBtDvlkOtYlWCinUdNBx9"
    },
    # Add more servers here
}

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

    users_list = response.json().get("users", [])
    filtered_users = [user for user in users_list if "@kasm.local" not in user.get("username")]
    return filtered_users


@app.route('/')
def dashboard():
    users_per_server = {}
    for server, server_info in KASM_SERVERS.items():
        api_key = server_info["api_key"]
        api_key_secret = server_info["api_key_secret"]
        users = get_users(api_key, api_key_secret, server)
        users_per_server[server] = [user["username"] for user in users]

    return render_template('dashboard.html', users_per_server=users_per_server)

if __name__ == '__main__':
    app.run(debug=True)