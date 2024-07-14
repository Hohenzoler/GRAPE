import requests
import time
#
# with open('github-api-handling/releases.txt', 'w') as f:
#     f.close()

dir = 'github-api-handling/releases.txt'

def get_all_releases(token, placeholder=None):
    a = update()
    print(a)
    if placeholder != None or a:
        api_url = f"https://api.github.com/repos/hohenzoler/grape/releases"

        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            releases_info = response.json()
            releases = []
            with open(dir, 'w') as f:
                f.write(f"{str(time.time())}\n")
                for release in releases_info:
                    try:
                        browser_link = release.get('assets', 'N/A')
                        try:
                            browser_link = browser_link[1]['browser_download_url']
                        except:
                            browser_link = browser_link[0]['browser_download_url']
                    except:
                        browser_link = 'N/A'
                    f.write(f"{release.get('tag_name', 'N/A')}\n")
                    releases.append(release.get('tag_name', 'N/A'))
                f.close()
        else:
            releases = []
            with open(dir, 'r') as f:
                for line in f:
                    line = line.strip()
                    releases.append(line)
                releases.pop(0)
                f.close()
    else:
        releases = []
        with open(dir, 'r') as f:
            for line in f:
                line = line.strip()
                releases.append(line)
            releases.pop(0)
            f.close()

    return releases



def update():
    try:
        with open(dir, 'r') as f:
            time1 = f.readline()
            time1 = float(time1)
            f.close()
            if time.time() - time1 >= 3600:
                return True
            return False
    except:

        return True