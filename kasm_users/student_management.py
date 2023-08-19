import csv
import requests

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

LOG_FILE = "user_creation_log.md"
DATA_FILE = "data.csv"
MAX_USERS_PER_SERVER = 5

# Initialize user count, server index, and users per server
user_counts = {server_url: 0 for server_url in KASM_SERVERS}
server_list = list(KASM_SERVERS.keys())
current_server_index = 0
users_per_server = {server_url: [] for server_url in KASM_SERVERS}

with open(LOG_FILE, 'w') as f:
    pass  # Clear the log file

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
