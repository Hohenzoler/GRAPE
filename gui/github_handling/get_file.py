import requests
import os
from zipfile import ZipFile

download_path = 'versions'
onefile = 'onefile'

def download_release_file(release_tag, file_name):
    api_url = f"https://api.github.com/repos/hohenzoler/grape/releases/tags/{release_tag}"
    response = requests.get(api_url)
    if response.status_code == 200:
        release_info = response.json()
        assets = release_info['assets']
        file_found = False
        for asset in assets:
            if not onefile in asset['name']:
                file_name = asset['name']
                file_found = True
                asset_url = asset['browser_download_url']
                download_url(asset_url, os.path.join(download_path, f'{release_tag}.zip'))
                print(f"File '{file_name}' downloaded successfully.")
                break
        if not file_found:
            print(f"File '{file_name}' not found in the release.")
        else:
            extract_files(file_name, release_tag)
            return 'success!'


    else:
        print(f"Failed to download release. Status code: {response.status_code}")

def download_url(url, save_path, chunk_size=128):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=chunk_size):
                f.write(chunk)
def extract_files(file_name, tag):
    # print(f'{download_path}/{name}')
    print(f'{download_path}/{tag}.zip')
    with ZipFile(f'{download_path}/{tag}.zip', 'r') as zobject:
        zobject.extractall(f"{download_path}/{tag})")

