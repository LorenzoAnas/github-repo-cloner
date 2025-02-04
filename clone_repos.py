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

def interactive_menu(repos):
    """Presents the user with a terminal UI to choose repositories to update/download."""
    while True:
        print("\nSelect an option:")
        print("1. Download/Update ALL repositories")
        print("2. Download/Update a specific repository")
        print("3. Quit")
        choice = input("Enter your selection: ").strip()

        if choice == "1":
            for repo in repos:
                clone_or_update_repo(repo["clone_url"], repo["name"])
            print("All repositories processed.")
        elif choice == "2":
            print("\nAvailable repositories:")
            for index, repo in enumerate(repos):
                print(f"[{index}] {repo['name']}")
            selection = input("Enter the repository number or name (exact): ").strip()
            repo = None
            if selection.isdigit():
                idx = int(selection)
                if 0 <= idx < len(repos):
                    repo = repos[idx]
            else:
                # match repository by name
                for r in repos:
                    if r["name"] == selection:
                        repo = r
                        break
            if repo:
                clone_or_update_repo(repo["clone_url"], repo["name"])
            else:
                print("Invalid repository selection.")
        elif choice == "3":
            print("Exiting menu.")
            break
        else:
            print("Invalid option. Please try again.")

def main():
    os.makedirs(DESTINATION_DIR, exist_ok=True)

    # Verify token validity
    verify_token()

    print("Fetching repositories...")
    response = requests.get(GITHUB_API_URL, auth=(USERNAME, TOKEN))
    if response.status_code != 200:
        print(f"Failed to fetch repositories: {response.status_code}")
        print(response.json())
        return

    repos = response.json()
    # Check if any repositories were returned
    if not repos:
        print("No repositories found for the user.")
        return

    interactive_menu(repos)
    
if __name__ == "__main__":
    main()
