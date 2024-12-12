# GitHub Repository Cloner

This script automatically clones or updates all repositories from your GitHub account to a local drive.

## Features
- Fetches all repositories for a given GitHub user.
- Clones repositories that don't exist locally.
- Updates repositories that are already cloned.

## Requirements
- Python 3.6 or later
- Git installed and added to the system's PATH
- A GitHub personal access token

## Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/github-repo-cloner.git
   cd github-repo-cloner
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add the following variables:
   ```env
   GITHUB_USERNAME=your_github_username
   GITHUB_TOKEN=your_personal_access_token
   DESTINATION_DIR=/path/to/local/drive
   ```

4. Run the script:
   ```bash
   python clone_repos.py
   ```

## Notes
- Make sure your GitHub token has the required permissions (e.g., `repo` scope for private repositories).
- The script will skip updating repositories if they already exist locally.

## Contributing
Feel free to fork this repository and make pull requests to enhance the script!

## License
MIT License
```
