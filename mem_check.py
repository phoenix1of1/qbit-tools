import requests

# Configuration
qbittorrent_url = 'http://localhost:8080'  # Replace with your qBittorrent Web UI URL
username = 'your_user_name'  # Replace with your qBittorrent username
password = 'your_password'  # Replace with your qBittorrent password
tag_to_search = 'your_tag'  # Replace with the tag you want to search for

# Authenticate with qBittorrent
login_url = f'{qbittorrent_url}/api/v2/auth/login'
login_data = {
    'username': username,
    'password': password
}
session = requests.Session()
response = session.post(login_url, data=login_data)

if response.status_code == 200:
    print("Successfully authenticated with qBittorrent")
else:
    print("Failed to authenticate with qBittorrent")
    exit(1)

# Fetch the list of torrents with the specific tag
torrents_url = f'{qbittorrent_url}/api/v2/torrents/info?filter=all&tag={tag_to_search}'
response = session.get(torrents_url)

if response.status_code == 200:
    torrents = response.json()
    total_size = sum(torrent['total_size'] for torrent in torrents)
    total_size_gb = total_size / (1024 ** 3)  # Convert bytes to gigabytes
    print(f"Total size of torrents with tag '{tag_to_search}': {total_size_gb:.2f} GB")
else:
    print("Failed to fetch torrents information")
