import csv
import requests
import os
import json

KASM_SERVERS = {
    "https://kasm100.nighthawkcodingsociety.com": {
        "api_key": "UmJYml6vlGtu",
        "api_key_secret": "UKPCWqwjilQeyXR2tnjw3sixZqc88W28"
    },
    "https://kasm101.nighthawkcodingsociety.com": {
        "api_key": "L1gkinqZtvbH",
        "api_key_secret": "WAKK9Gcl6dNtP025P9DV7EOoeESEYiYH"
    },
    "https://kasm102.nighthawkcodingsociety.com": {
        "api_key": "YbUxUHQ3Heg0",
        "api_key_secret": "E4ntLqE25sN01NXYWgtQRgsAO35rlI3i"
    },
    "https://kasm103.nighthawkcodingsociety.com": {
        "api_key": "MbGuTxwwfK22",
        "api_key_secret": "8htknVwcD1IjNnKbCWdXYkiETBSvJIHC"
    },
    "https://kasm104.nighthawkcodingsociety.com": {
        "api_key": "OyLpqUBgaMyu",
        "api_key_secret": "8TtliJrG3yXqusYJUVlaXcN7vriDOvQi"
    },
    "https://kasm200.nighthawkcodingsociety.com": {
        "api_key": "ra2TtCl5EIlO",
        "api_key_secret": "zFnJiZXN1Q896ueKHOylVYzYSVqPyFlT"
    },
    "https://kasm201.nighthawkcodingsociety.com": {
        "api_key": "kOH4x0On5Y7e",
        "api_key_secret": "9URSa9HlpbltQuAKGXCUCuPdEM7hdtMC"
    },
    "https://kasm202.nighthawkcodingsociety.com": {
        "api_key": "dTvDmN3qidW7",
        "api_key_secret": "ApUtxuLmHzsqRu5BEmjAqjdwtNGUlAyo"
    },
    "https://kasm203.nighthawkcodingsociety.com": {
        "api_key": "7ROHR5nCNG4o",
        "api_key_secret": "j3n9gJhZaza8IW5FBRGnPy4sqvmkW3su"
    },
    "https://kasm300.nighthawkcodingsociety.com": {
        "api_key": "moERAHkP0LEB",
        "api_key_secret": "IERMN6c0NDKOTeEsxASb2vasify2tql5"
    },
    "https://kasm301.nighthawkcodingsociety.com": {
        "api_key": "t1eAKEGd4GNE",
        "api_key_secret": "CW5vSYtPu8LliT2ipKZifpbCzVsLpjA8"
    },
}

## update kasm servers from json file if it exists
try:
    with open('../kasm.json') as f:
        KASM_SERVERS = json.load(f)
except:
    # file doesnt exist/malformed
    pass

LOG_FILE = "user_creation_log.md"
DATA_FILE = "data.csv"
MAX_USERS_PER_SERVER = 5

# Initialize user count, server index, and users per server
user_counts = {server_url: 0 for server_url in KASM_SERVERS}
server_list = list(KASM_SERVERS.keys())
current_server_index = 0
users_per_server = {server_url: [] for server_url in KASM_SERVERS}

# check if the log file exists, if not, create it
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, 'a') as f:
        f.write("| First Name | Last Name | Username | Server | Status |\n")
        f.write("| --- | --- | --- | --- | --- |\n")

def create_user(api_key, api_key_secret, user_data, api_base_url):
    endpoint = f"{api_base_url}/api/public/create_user"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "api_key": api_key,
        "api_key_secret": api_key_secret,
        "target_user": user_data
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    return response.json()

def get_users_count(api_key, api_key_secret, api_base_url):
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
    print(f"Users on {api_base_url}: {len(filtered_users)}")
    return len(filtered_users)

def log_status(user_data, api_base_url, status, log_file):
    with open(log_file, 'a') as f:
        f.write(f"| {user_data['first_name']} | {user_data['last_name']} | {user_data['username']} | {api_base_url} | {status} |\n")

def main():
    global current_server_index  # Declare current_server_index as global

    # Read user data from the CSV file
    with open(DATA_FILE, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            user_data = {
                "username": row['uid'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "locked": False,
                "password": "123Qwerty!",
                "disabled": False
            }

            while True:
                api_base_url = server_list[current_server_index]
                users_count = get_users_count(KASM_SERVERS[api_base_url]['api_key'], KASM_SERVERS[api_base_url]['api_key_secret'], api_base_url)

                if users_count < 0:
                    break  # Exit the loop if there's an issue with user count retrieval

                if users_count == 5:
                    current_server_index = (current_server_index + 1) % len(server_list)
                    continue  # Move to the next server

                if user_counts[api_base_url] < MAX_USERS_PER_SERVER and users_count < MAX_USERS_PER_SERVER:
                    response = create_user(KASM_SERVERS[api_base_url]['api_key'], KASM_SERVERS[api_base_url]['api_key_secret'], user_data, api_base_url)
                    status = response.get('status') if response.get('status') == 'success' else f"Error: {response.get('error_message')}"

                    user_counts[api_base_url] += 1
                    users_per_server[api_base_url].append(user_data['username'])
                    log_status(user_data, api_base_url, status, LOG_FILE)
                else:
                    current_server_index = (current_server_index + 1) % len(server_list)
                    continue  # Move to the next server

                current_server_index = (current_server_index + 1) % len(server_list)
                break  # Move to the next user

if __name__ == "__main__":
    main()
