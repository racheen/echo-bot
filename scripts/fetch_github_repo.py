import requests
import os

def fetch_github_repos(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)
    response.raise_for_status()
    repos = response.json()
    return [{"name": repo["name"], "default_branch": repo["default_branch"]} for repo in repos]


def fetch_and_save_readme(username, repo_name, default_branch, output_dir="github_txts"):
    readme_url = f"https://raw.githubusercontent.com/{username}/{repo_name}/{default_branch}/readme.md"
    response = requests.get(readme_url)
    
    if response.status_code == 200:
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, f"{repo_name}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Saved: {file_path}")
    else:
        print(f"❌ No README.md for {repo_name}")

username = "racheen"
repos = fetch_github_repos(username)

for repo in repos:
    fetch_and_save_readme(username, repo["name"], repo["default_branch"])

