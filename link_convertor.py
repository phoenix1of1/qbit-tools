import os
import requests

# Configuration
qbittorrent_url = 'http://localhost:8080'  # Replace with your qBittorrent Web UI URL
username = 'your_username'  # Replace with your qBittorrent username
password = 'your_password'  # Replace with your qBittorrent password

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

# Fetch the list of torrents with the "linked" tag
torrents_url = f'{qbittorrent_url}/api/v2/torrents/info?filter=all&tag=linked'
response = session.get(torrents_url)

if response.status_code == 200:
    torrents = response.json()
    for torrent in torrents:
        torrent_hash = torrent['hash']
        files_url = f'{qbittorrent_url}/api/v2/torrents/files?hash={torrent_hash}'
        files_response = session.get(files_url)

        if files_response.status_code == 200:
            files = files_response.json()
            for file in files:
                file_path = file['name']
                full_path = os.path.join(torrent['save_path'], file_path)
                try:
                    if os.path.islink(full_path):
                        print(f"File is already a symlink: {full_path}")
                    elif os.stat(full_path).st_nlink > 1:
                        # Convert hardlink to symlink
                        original_path = os.path.realpath(full_path)
                        os.remove(full_path)
                        os.symlink(original_path, full_path)
                        print(f"Converted hardlink to symlink: {full_path}")
                except FileNotFoundError:
                    print(f"File not found: {full_path}")
else:
    print("Failed to fetch torrents information")
