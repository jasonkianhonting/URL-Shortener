from functools import wraps
from flask import jsonify, redirect
import requests

loggedStatus = ""
guid = ""
headers = ""

# Ensures that certain pages can only be accessed after loggin in


def required_login(f):
    """View decorator for requiring a user to have an initialized session

    Returns:
        Redirect to `/login` if not logged in, otherwise allow view
    """
    @wraps(f)
    def wrap(*args, **kwargs):
        if loggedStatus == True:
            return f(*args, **kwargs)
        else:
            return redirect('/')
    return wrap


# Login functionaltiy from the Bitly API
def login(email, password):
    res_auth = requests.post(
        "https://api-ssl.bitly.com/oauth/access_token", auth=(email, password))
    print("Authorising, please wait for a moment")
    if res_auth.status_code == 200:
        # if response is OK, get the access token
        access_token = res_auth.content.decode()
        print("Access Granted")
        # construct the request headers with authorization
        global headers
        headers = {"Authorization": f"Bearer {access_token}"}

        # get the group UID associated with my account
        res_group = requests.get(
            "https://api-ssl.bitly.com/v4/groups", headers=headers)
        if res_group.status_code == 200:
            # if response is OK, get the GUID
            data_groups = res_group.json()['groups'][0]
            global guid
            guid = data_groups['guid']
            global loggedStatus
            loggedStatus = data_groups['is_active']
            return True

        else:
            return jsonify({"error": "Wrong Username or Password"}), 404
    else:
        return jsonify({"error": "Wrong Username or Password"}), 404


#Shortening function 
def shorten(value_link):
    link = ""
    shorten_res = requests.post("https://api-ssl.bitly.com/v4/shorten",
                                json={"group_guid": guid, "long_url": value_link}, headers=headers)
    if shorten_res.status_code == 200 or 201:
        # if response is OK, get the shortened URL
        link = shorten_res.json().get("link")
        return link
    else:
        return link


def Logout():
    global loggedStatus
    loggedStatus = ""
    return loggedStatus
