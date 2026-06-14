import httpx 
import urllib.parse

LINKEDIN_CLIENT_ID ="86ws0qqnvfn8de"
LINKEDIN_CLIENT_SECRET ="your_client_secret_here"

def generate_access_token() -> str:
    url = "https://www.linkedin.com/oauth/v2/accessToken"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    response = httpx.post(url, headers=headers, data=data)
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"Error from LinkedIn API: {response.text}")
        raise e
        
    return response.json()["access_token"]


if __name__ == "__main__":
    token = generate_access_token()
    print(token)
   