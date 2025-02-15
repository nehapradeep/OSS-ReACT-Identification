import base64
import os
import requests

repos = [
    # {'owner': 'Kanaries', 'repo': 'pygwalker'},
    {'owner': 'apache', 'repo': 'incubator-resilientdb'},
    {'owner': 'apache', 'repo': 'kvrocks'},
    {'owner': 'apache', 'repo': 'doris'},
    {'owner': 'apache', 'repo': 'celeborn'}
]
token = None or os.environ['GITHUB_TOKEN']


headers = {
    'Authorization': f'token {token}'
}

def get_pull_requests(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/pulls?q=is%3Apr+is%3Aclosed+is%3Aopen'
    params = {
        "state": "all",  # Get both open and closed PRs
        "per_page": 100,  # Maximum per request
        "page": 1
    }
    all_prs = []
    
    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        prs = response.json()
        if not prs:
            break  # Stop when there are no more PRs
        
        all_prs.extend(prs)
        params["page"] += 1
        
    with open(f'github_api/{repo}/pr.txt', "w", encoding="utf-8") as file:
        for pr in all_prs:
            file.write(f"PR #{pr['number']}: {pr['title']} (State: {pr['state']})\n")
            file.write(f"URL: {pr['html_url']}\n")
            file.write(f"Created at: {pr['created_at']}, Merged at: {pr.get('merged_at', 'Not merged')}\n")
            file.write("=" * 80 + "\n")

    return all_prs

def get_pull_request_comments(owner, repo, pr_number):
    url = f'https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments'
    response = requests.get(url, headers=headers)
    return response.json()

def get_issues(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    response = requests.get(url, headers=headers)
    return response.json()

def get_file_path(owner, repo, file_path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.get(url, headers=headers)
    data = response.json()
    with open(f"github_api/{repo}/{file_path}", "w", encoding="utf-8") as file:
        if 'content' in data:
            file_content = base64.b64decode(data["content"]).decode("utf-8")
            file.write(file_content)
        else:
            file.write(f"File {file_path} not found in the repository.")

def get_issue_comments(owner, repo, issue_number):
    url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments'
    response = requests.get(url, headers=headers)
    return response.json()

def get_discussions(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/discussions'
    response = requests.get(url, headers=headers)
    return response.json()

if __name__ == "__main__":
    for repo in repos:
        os.makedirs(os.path.join('github_api',repo['repo']), exist_ok=True)
        print(f"Processing repo: {repo['owner']}/{repo['repo']}")
        get_file_path(repo['owner'], repo['repo'], 'README.md')
        get_file_path(repo['owner'], repo['repo'], 'CONTRIBUTING.md')
        get_file_path(repo['owner'], repo['repo'], 'LICENSE')
        pull_requests = get_pull_requests(repo['owner'], repo['repo'])
        with open(f'github_api/{repo['repo']}/pr_comments.txt', 'w') as f:
            for pr in pull_requests:
                pr_number = pr['number']
                pr_comments = get_pull_request_comments(repo['owner'], repo['repo'], pr_number)
                # print(f"Comments for PR {pr_number}: {pr_comments}")
                if len(pr_comments) > 0:
                    f.write(f"Comments for PR {pr_number}: {pr_comments}\n")
            
        with open(f'github_api/{repo['repo']}/issue_comments.txt', 'w') as f:
            issues = get_issues(repo['owner'], repo['repo'])
            for issue in issues:
                issue_number = issue['number']
                issue_comments = get_issue_comments(repo['owner'], repo['repo'], issue_number)
                # print(f"Comments for Issue {issue_number}: {issue_comments}")
                if len(issue_comments) > 0:
                    f.write(f"Comments for Issue {issue_number}: {issue_comments}\n")
            
        with open(f'github_api/{repo['repo']}/discussions.txt', 'w') as f:
            discussions = get_discussions(repo['owner'], repo['repo'])
            # print(f"Discussions: {discussions}")
            f.write(f"Discussions: {discussions}\n")
