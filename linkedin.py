import requests

# Set your LinkedIn app credentials
client_id = "782sxestg41apo"
client_secret = "WPL_AP1.9jZXCnZgtld9N44V.PowacQ=="

# LinkedIn token endpoint
url = "https://www.linkedin.com/oauth/v2/accessToken"

# Define the request parameters
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret
}

# Make the POST request
response = requests.post(url, data=data)

# Check the response
if response.status_code == 200:
    access_token = response.json().get("access_token")
    print(f"Access Token: {access_token}")
else:
    print(f"Failed to retrieve access token: {response.status_code}, {response.text}")