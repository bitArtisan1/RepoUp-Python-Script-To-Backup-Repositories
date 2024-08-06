import os
import subprocess
import requests
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init()

# Logging function with color support
def log(message, level="INFO"):
    levels = {
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "SUCCESS": Fore.BLUE
    }
    color = levels.get(level, Fore.WHITE)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{Fore.CYAN}[{timestamp}]{Style.RESET_ALL} {color}[{level}]{Style.RESET_ALL} {message}")

# Function to get all repositories for a user
def get_repositories(username):
    api_url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(api_url)
    if response.status_code != 200:
        log(f"Failed to get repositories for user {username}. HTTP Status Code: {response.status_code}", "ERROR")
        response.raise_for_status()
    return response.json()

# Function to get all releases for a repository
def get_releases(username, repo_name):
    api_url = f"https://api.github.com/repos/{username}/{repo_name}/releases"
    response = requests.get(api_url)
    if response.status_code != 200:
        log(f"Failed to get releases for repository {repo_name}. HTTP Status Code: {response.status_code}", "ERROR")
        response.raise_for_status()
    return response.json()

# Function to download release assets
def download_assets(releases, backup_dir):
    for release in releases:
        release_name = release["name"]
        assets = release["assets"]

        log(f"Backing up release: {release_name}", "INFO")

        for asset in assets:
            asset_name = asset["name"]
            asset_url = asset["browser_download_url"]

            log(f"  Downloading asset: {asset_name}", "INFO")

            try:
                response = requests.get(asset_url)
                response.raise_for_status()
                asset_path = backup_dir / asset_name
                with open(asset_path, "wb") as file:
                    file.write(response.content)
                log(f"Successfully downloaded asset: {asset_name}", "SUCCESS")
            except requests.exceptions.RequestException as e:
                log(f"Failed to download asset {asset_name}. Error: {e}", "ERROR")

# Function to clone repository as mirror and create bundle
def clone_and_bundle_repo(username, repo_name, repo_dir):
    repo_url = f"https://github.com/{username}/{repo_name}.git"
    mirror_dir = repo_dir / f"{repo_name}.git"

    log(f"Cloning repository {repo_name} as mirror", "INFO")
    result = subprocess.run(["git", "clone", "--mirror", repo_url, str(mirror_dir)], capture_output=True, text=True)
    if result.returncode != 0:
        log(f"Failed to clone repository {repo_name}. Error: {result.stderr}", "ERROR")
    else:
        log(f"Successfully cloned repository {repo_name}", "SUCCESS")

    log(f"Creating bundle for repository {repo_name}", "INFO")
    bundle_path = mirror_dir / f"{repo_name}.bundle"
    result = subprocess.run(["git", "--git-dir", str(mirror_dir), "bundle", "create", str(bundle_path), "--all"], capture_output=True, text=True)
    if result.returncode != 0:
        log(f"Failed to create bundle for repository {repo_name}. Error: {result.stderr}", "ERROR")
    else:
        log(f"Successfully created bundle for repository {repo_name}", "SUCCESS")

def main():
    # Prompt for the GitHub username
    github_username = input("Enter GitHub username: ")

    # Get all repositories for the user
    try:
        repositories = get_repositories(github_username)
    except requests.exceptions.RequestException as e:
        log(f"Failed to get repositories for user {github_username}. Error: {e}", "ERROR")
        return

    # Directory to store backups
    backup_base_dir = Path("backups") / github_username
    backup_base_dir.mkdir(parents=True, exist_ok=True)

    for repo in repositories:
        repo_name = repo["name"]

        # Directory for this repository's backup
        repo_backup_dir = backup_base_dir / repo_name
        repo_backup_dir.mkdir(parents=True, exist_ok=True)

        # Clone and bundle the repository
        try:
            clone_and_bundle_repo(github_username, repo_name, repo_backup_dir)
        except subprocess.CalledProcessError as e:
            log(f"Failed to clone and bundle repository {repo_name}. Error: {e}", "ERROR")
            continue

        # Get and download release assets
        try:
            releases = get_releases(github_username, repo_name)
            if releases:
                release_backup_dir = repo_backup_dir / "releases"
                release_backup_dir.mkdir(parents=True, exist_ok=True)
                download_assets(releases, release_backup_dir)
            else:
                log(f"No releases found for repository: {repo_name}", "WARNING")
        except requests.exceptions.RequestException as e:
            log(f"Failed to get releases for repository {repo_name}. Error: {e}", "ERROR")

    log("Backup completed!", "INFO")

if __name__ == "__main__":
    main()