import requests

with requests.session as s:
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 '
                      'Safari/537.36 '
    }
    url = "https://app.woodpecker.co/login"
    r = s.get(url, headers=headers)

    print(r.content)