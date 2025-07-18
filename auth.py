import requests 


def login(login_email, password, api_key):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"
    payload = {
        "email": login_email,
        "password": password,
        "returnSecureToken": True,
    }
    resp = requests.post(url, json=payload)
    return resp.json() if resp.status_code == 200 else None
