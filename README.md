<p align="center">
  <a href="https://ko-fi.com/D1D11CZNM1">
    <img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="Support me on Ko-fi" />
  </a>
</p>

# RepoUp

RepoUp is a Python tool/script that automates the backup of GitHub repositories for a user. It clones repositories, creates bundles, and downloads release assets, providing a comprehensive backup solution.

<div align="center">
  <img src="https://github.com/user-attachments/assets/f02f5dd8-b411-4bd5-b3a2-0a335d771fb0" alt="netDigger Logo" width="500px" />
  <p><strong><em>Python Script For Fully Backing Up Repositories Automatically.</em></strong></p>
</div>


## Features

- **Clone Repositories**: Clone GitHub repositories as mirrors.
- **Create Bundles**: Bundle cloned repositories for easy storage and transfer.
- **Download Assets**: Download release assets for each repository.
- **Detailed Logging**: Provides informative and colored logs for better readability and debugging.

## Installation

1. **Clone the RepoUp Repository**
    ```bash
    git clone https://github.com/bitArtisan1/RepoUp-Python-Script-To-Backup-Repositories.git
    cd RepoUp
    ```

2. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run RepoUp**
    ```bash
    python repoup.py
    ```

2. **Follow the Prompts**
    - Enter the GitHub username when prompted.
    - The script will automatically fetch the repositories and begin the backup process.

## Handling Rate Limits

RepoUp uses the GitHub API, which has rate limits. If you encounter rate limit errors, consider:

- **Using Authentication**: Add your GitHub token to the requests to increase rate limits.
- **Spacing Requests**: Avoid running the script multiple times in quick succession.
- **Checking GitHub API Status**: Ensure the GitHub API is not experiencing issues.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Support Me
If you find RepoUp useful, consider supporting me by:

- Starring the repository on GitHub
- Sharing the tool with others
- Providing feedback and suggestions
- Follow me for more :)

<a href="https://ko-fi.com/D1D11CZNM1">
  <img src="https://github.com/user-attachments/assets/ba118768-9054-416f-b7b2-adaa69a53434" alt="Support me on Ko-fi" width="200" />
</a>
    
---
For any issues or feature requests, please open an issue on GitHub. Happy coding!

