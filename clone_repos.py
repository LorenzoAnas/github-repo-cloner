import os
import requests
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

USERNAME = os.getenv("GITHUB_USERNAME")
TOKEN = os.getenv("GITHUB_TOKEN")
DESTINATION_DIR = os.getenv("DESTINATION_DIR")

if not all([USERNAME, TOKEN, DESTINATION_DIR]):
    raise ValueError("Please ensure GITHUB_USERNAME, GITHUB_TOKEN, and DESTINATION_DIR are set in the .env file.")

# Use the authenticated endpoint to include private repositories
GITHUB_API_URL = "https://api.github.com/user/repos"

def verify_token():
    """Verify if the provided token is valid and has the correct permissions."""
    print("Verifying GitHub token...")
    response = requests.get("https://api.github.com/user", auth=(USERNAME, TOKEN))
    if response.status_code == 200:
        user_data = response.json()
        print(f"Token is valid. Logged in as: {user_data['login']}")
    else:
        print(f"Failed to verify token: {response.status_code} - {response.json().get('message', 'Unknown error')}")
        raise Exception("Invalid or insufficient token permissions. Please reconfigure your token.")

def clone_or_update_repo(repo_url, repo_name):
    """Clones or updates a Git repository."""
    repo_path = os.path.join(DESTINATION_DIR, repo_name)
    if os.path.exists(repo_path):
        print(f"Updating {repo_name}...")
        try:
            subprocess.run(["git", "-C", repo_path, "pull"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to update {repo_name}: {e}")
    else:
        print(f"Cloning {repo_name}...")
        subprocess.run(["git", "clone", repo_url, repo_path], check=True)

def main():
    os.makedirs(DESTINATION_DIR, exist_ok=True)

    # Verify token validity
    verify_token()

    print("Fetching repositories...")
    # Authenticated request to fetch all repositories, including private ones
    response = requests.get(GITHUB_API_URL, auth=(USERNAME, TOKEN))
    if response.status_code != 200:
        print(f"Failed to fetch repositories: {response.status_code}")
        print(response.json())
        return

    repos = response.json()
    for repo in repos:
        repo_name = repo["name"]
        repo_url = repo["clone_url"]
        clone_or_update_repo(repo_url, repo_name)

    print("All repositories are up to date.")

if __name__ == "__main__":
    main()
