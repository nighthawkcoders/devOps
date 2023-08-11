import csv
import requests

KASM_SERVERS = {
    "https://kasm100.nighthawkcodingsociety.com": {
        "api_key": "OmjrGQWTfo6p",
        "api_key_secret": "sedDY5j3QhKLADrI6Xlge6Fak0ZHKQwI"
    },
    "https://kasm101.nighthawkcodingsociety.com": {
        "api_key": "phMV1dCgGFO8",
        "api_key_secret": "7JPrjw2VCOnyMxADOZLXczlpTww9kbaX"
    },
    # Add more servers here
}

LOG_FILE = "user_creation_log.md"
DATA_FILE = "data.csv"
MAX_USERS_PER_SERVER = 5

with open(LOG_FILE, 'w') as f:
    pass  # Clear the log file

with open(LOG_FILE, 'a') as f:
    f.write("| First Name | Last Name | Server | Status |\n")
    f.write("| --- | --- | --- | --- |\n")
# Initialize user count for each server
user_counts = {server_url: 0 for server_url in KASM_SERVERS}
users_per_server = {server_url: [] for server_url in KASM_SERVERS}


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

def log_status(user_data, api_base_url, status, log_file):
    with open(log_file, 'a') as f:
        f.write(f"| {user_data['first_name']} | {user_data['last_name']} | {api_base_url} | {status} |\n")

def main():
    # Read user data from the CSV file
    with open(DATA_FILE, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            username = row['first_name'].lower() + row['last_name'].lower()

            user_data = {
                "username": username,
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "locked": False,
                "disabled": False
            }

            for api_base_url, server_info in KASM_SERVERS.items():
                if user_counts[api_base_url] < MAX_USERS_PER_SERVER and user_data['username'] not in users_per_server[api_base_url]:
                    response = create_user(server_info['api_key'], server_info['api_key_secret'], user_data, api_base_url)
                    status = response.get('status') if response.get('status') == 'success' else f"Error: {response.get('error_message')}"

                    user_counts[api_base_url] += 1
                    users_per_server[api_base_url].append(user_data['username'])
                    log_status(user_data, api_base_url, status, LOG_FILE)
                    break  # Move to the next user if added to this server

if __name__ == "__main__":
    main()
