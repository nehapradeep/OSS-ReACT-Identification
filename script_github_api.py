import base64
import os
import requests
from datetime import datetime, timedelta

repos = [
    # {'owner': 'Kanaries', 'repo': 'pygwalker'},
    #{'owner': 'apache', 'repo': 'incubator-resilientdb'},
    #{'owner': 'apache', 'repo': 'kvrocks'},
    #{'owner': 'apache', 'repo': 'openDAL'},
    # {'owner': 'apache', 'repo': 'doris'},
    # {'owner': 'apache', 'repo': 'incubator-liminal'},
    #{'owner': 'apache', 'repo': 'celeborn'}
    #{'owner': 'apache', 'repo': 'superset'},
    #{'owner': 'apache', 'repo': 'echarts'},
    # {'owner': 'apache', 'repo': 'spark'}
    {'owner': 'apache', 'repo': 'airflow'}

]
token = None or os.environ['GITHUB_TOKEN']


headers = {
    'Authorization': f'token {token}'
}

import requests

response = requests.get("https://api.github.com/rate_limit")
print(response.json())

# Get the date 6 months ago
six_months_ago = (datetime.utcnow() - timedelta(days=180)).isoformat() + "Z"

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
        
        # Filter issues by created_at timestamp
        filtered_prs = [pr for pr in prs if pr["created_at"] >= six_months_ago]
        all_prs.extend(filtered_prs)
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

# def get_issues(owner, repo):
#     url = f'https://api.github.com/repos/{owner}/{repo}/issues'
#     response = requests.get(url, headers=headers)
#     return response.json()

#pranav
def get_issues(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    params = {"state": "all", "per_page": 100, "page": 1}
    all_issues = []
    
    while True:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        
        issues = response.json()
        if not issues:
            break
        
        # Filter issues by created_at timestamp
        filtered_issues = [issue for issue in issues if issue["created_at"] >= six_months_ago]
        all_issues.extend(filtered_issues)
        params["page"] += 1
        if len(issues) < 100:
            break
    
    return all_issues

def get_file_path(owner, repo, file_path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.get(url, headers=headers)
    data = response.json()

    # Ensure all parent directories exist
    full_path = os.path.join('github_api', repo, file_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)

    with open(full_path, "w", encoding="utf-8") as file:
        if 'content' in data:
            file_content = base64.b64decode(data["content"]).decode("utf-8")
            file.write(file_content)
        else:
            file.write(f"File {file_path} not found in the repository.")

def get_src_code_path(owner, repo, file_path):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
    response = requests.get(url, headers=headers)
    data = response.json()
    
    # Define a strict save directory (`github_api/{repo}/top_files/`)
    save_dir = os.path.join('github_api', repo, 'top_files')
    #save_dir = os.path.join('github_api', 'ResDB', 'top_files')
    os.makedirs(save_dir, exist_ok=True)

    # Extract filename from original path and save only in `top_files/`
    filename = os.path.basename(file_path)  # Get file name without path
    save_path = os.path.join(save_dir, filename)  # Save inside `top_files/`

    with open(save_path, "w", encoding="utf-8") as file:
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

#pranav_start
def get_top_source_files(owner, repo):
    # for kvrocks their main branch is "unstable"
    #url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/unstable?recursive=1'
    url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1'
    # It's "main" for openDAL
    #url = f'https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    tree = response.json().get('tree', [])
    
    source_files = [file['path'] for file in tree if file['path'].endswith(('.c', '.cpp', '.py', '.java', '.js', '.go'))]
    file_lengths = []
    
    for file_path in source_files:
        file_url = f'https://api.github.com/repos/{owner}/{repo}/contents/{file_path}'
        file_response = requests.get(file_url, headers=headers)
        file_data = file_response.json()
        
        if 'content' in file_data:
            content = base64.b64decode(file_data['content']).decode('utf-8')
            line_count = len(content.splitlines())
            file_lengths.append((file_path, line_count))

    file_lengths.sort(key=lambda x: x[1], reverse=True)
    top_files = file_lengths[:max(1, len(file_lengths) // 10)]
    
    os.makedirs(f'github_api/{repo}/top_files', exist_ok=True)
    #os.makedirs(f'github_api/ResDB/top_files', exist_ok=True)
    for file_path, _ in top_files:
        get_src_code_path(owner, repo, file_path)
    
    return top_files
#pranav_end

if __name__ == "__main__":
    for repo in repos:
        os.makedirs(os.path.join('github_api',repo['repo']), exist_ok=True)
        print(f"Processing repo: {repo['owner']}/{repo['repo']}")
        # get_file_path(repo['owner'], repo['repo'], 'README.md')
        # get_file_path(repo['owner'], repo['repo'], 'CONTRIBUTING.md')
        # get_file_path(repo['owner'], repo['repo'], 'LICENSE')
        # pull_requests = get_pull_requests(repo['owner'], repo['repo'])
        # with open(f'github_api/{repo["repo"]}/pr_comments.txt', 'w', encoding="utf-8") as f:
        #     for pr in pull_requests:
        #         pr_number = pr['number']
        #         pr_comments = get_pull_request_comments(repo['owner'], repo['repo'], pr_number)
        #         # print(f"Comments for PR {pr_number}: {pr_comments}")
        #         if len(pr_comments) > 0:
        #             f.write(f"Comments for PR {pr_number}: {pr_comments}\n")

        # with open(f'github_api/{repo["repo"]}/issue_comments.txt', 'w', encoding="utf-8", errors="ignore") as f:
        # #with open(f'github_api/ResDB/issue_comments.txt', 'w', encoding="utf-8") as f:
        #     issues = get_issues(repo['owner'], repo['repo'])
        #     for issue in issues:
        #         issue_number = issue['number']
        #         issue_labels = [label['name'] for label in issue.get('labels', [])]
        #         issue_comments = get_issue_comments(repo['owner'], repo['repo'], issue_number)
        #         f.write(f"Issue #{issue_number}: Labels: {', '.join(issue_labels) if issue_labels else 'No Labels'}\n")
        #         if issue_comments:
        #             f.write(f"Comments: {issue_comments}\n")
            
        # with open(f'github_api/{repo["repo"]}/discussions.txt', 'w', encoding="utf-8") as f:
        #     discussions = get_discussions(repo['owner'], repo['repo'])    
        #     # print(f"Discussions: {discussions}")
        #     f.write(f"Discussions: {discussions}\n")

        #pranav
        top_files = get_top_source_files(repo['owner'], repo['repo'])
        print(f"Top files: {top_files}")
        
