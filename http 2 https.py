import requests

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)'}

def check_https_redirection(url, headers=headers):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url
    try:
        with requests.get(url, headers=headers, allow_redirects=False) as response:
            if 300 <= response.status_code < 400 and "Location" in response.headers:
                redirect_url = response.headers["Location"]
                if redirect_url.startswith("https://"):
                    return True, redirect_url
            return False, None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return False, None

# Read the list of websites from a text file
with open('input', 'r') as file:
    websites = [line.strip() for line in file]

for website in websites:
    is_redirected, redirect_url = check_https_redirection(website)
    if is_redirected:
        print(f"{website} redirects to HTTPS. Redirect URL: {redirect_url}")
    else:
        print(f"{website} does not redirect to HTTPS")
