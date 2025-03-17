import csv
import os
from datetime import datetime, timedelta
import sys

#React 14
#React 62
#React 81
#React 9
#React 19
#React 33
#React 84


#neha
def analyze_react_14(csv_filename, output_file="final_react_analysis.csv"):
    pr_merge_times = []
    
    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            created_at = datetime.strptime(row["Created At"], "%Y-%m-%dT%H:%M:%SZ")
            merged_at = row["Merged At"]
            
            if merged_at != "None":
                merged_at = datetime.strptime(merged_at, "%Y-%m-%dT%H:%M:%SZ")
                pr_merge_times.append((merged_at - created_at).total_seconds())
    
    avg_merge_time = sum(pr_merge_times) / len(pr_merge_times) if pr_merge_times else None
    meets_criteria = avg_merge_time is not None and avg_merge_time <= 7 * 24 * 3600
    analysis = f"Meets criteria (Avg merge time: {avg_merge_time / 3600:.2f} hours)" if meets_criteria else f"Does not meet criteria (Avg merge time: {avg_merge_time / 3600:.2f} hours exceeds 7 days.)"
    recommendation = "Yes" if meets_criteria else "No"
    
    save_analysis("ReACT-14 Merge pull requests promptly.", analysis, recommendation, output_file)


#neha
def analyze_react_62(csv_filename, repo_creation_date, output_file="final_react_analysis.csv"):
    commit_timestamps = []
    
    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            commit_time = datetime.strptime(row["Author Date"], "%Y-%m-%d %H:%M:%S%z")
            commit_timestamps.append(commit_time)
    
    if commit_timestamps:
        first_commit_time = min(commit_timestamps)
        repo_creation_dt = datetime.strptime(repo_creation_date, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=commit_timestamps[0].tzinfo)
        meets_criteria = first_commit_time.year == repo_creation_dt.year and first_commit_time.month == repo_creation_dt.month
        
        two_months_later = repo_creation_dt + timedelta(days=60)
        commit_count = sum(1 for commit in commit_timestamps if repo_creation_dt <= commit <= two_months_later)
        contribution_rate_criteria = commit_count >= 20
        
        analysis = f"Meets criteria (Repo created: {repo_creation_dt}, First commit: {first_commit_time}, Contributions in first 2 months: {commit_count})" if meets_criteria and contribution_rate_criteria else f"Does not meet criteria (First commit date {first_commit_time} does not match repo creation month/year or insufficient contributions in first 2 months: {commit_count})"
    else:
        meets_criteria = False
        analysis = "Does not meet criteria (No commits found.)"
    
    recommendation = "Yes" if meets_criteria else "No"
    save_analysis("ReACT-62 Encourage developers to start contributing to the project early.", analysis, recommendation, output_file)

#neha
def analyze_react_81(commit_csv_filename, output_file="final_react_analysis.csv"):
    readme_updates = []
    
    with open(commit_csv_filename, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            if row["File Name"] == "README.md":
                commit_date = datetime.strptime(row["Author Date"], "%Y-%m-%d %H:%M:%S%z")
                readme_updates.append(commit_date)
    
    last_update = max(readme_updates) if readme_updates else None
    meets_criteria = last_update is not None and (datetime.now(last_update.tzinfo) - last_update).days <= 365
    analysis = f"Meets criteria (Last README update: {last_update})" if meets_criteria else "Does not meet criteria (README has not been updated in the last year.)"
    recommendation = "Yes" if meets_criteria else "No"
    
    save_analysis("ReACT-81 Keep knowledge up to date and findable.", analysis, recommendation, output_file)

#neha
def analyze_react_9(contrib_md_path, output_file="final_react_analysis.csv"):
    keyword = "how to request for access"
    analyze_contributing_react(contrib_md_path, "ReACT-9", keyword, output_file)

#neha
def analyze_react_19(contrib_md_path, output_file="final_react_analysis.csv"):
    keyword = "flag newcomers"
    analyze_contributing_react(contrib_md_path, "ReACT-19", keyword, output_file)

#neha
def analyze_react_33(contrib_md_path, output_file="final_react_analysis.csv"):
    keyword = "contribution guidelines"
    analyze_contributing_react(contrib_md_path, "ReACT-33", keyword, output_file)

#neha
def analyze_react_84(contrib_md_path, output_file="final_react_analysis.csv"):
    keyword = "onboarding support"
    analyze_contributing_react(contrib_md_path, "ReACT-84", keyword, output_file)

#neha
def analyze_contributing_react(contrib_md_path, react, keyword, output_file):
    try:
        with open(contrib_md_path, "r", encoding="utf-8") as file:
            content = file.read().lower()
            meets_criteria = keyword in content
            analysis = f"Meets criteria (Found keyword: '{keyword}')" if meets_criteria else f"Does not meet criteria (Keyword '{keyword}' not found)"
            recommendation = "Yes" if meets_criteria else "No"
            save_analysis(react, analysis, recommendation, output_file)
    except FileNotFoundError:
        print(f"Error: CONTRIBUTING.md file not found at {contrib_md_path}")

#neha
def save_analysis(react_name, outcome, recommendation, output_file):
    with open(output_file, mode="a", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["Project Name", "ReACT Name/Number", "Outcome", "Recommendation"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not os.path.isfile(output_file) or os.stat(output_file).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "Project Name": project_name,
            "ReACT Name/Number": react_name,
            "Outcome": outcome,
            "Recommendation": recommendation
        })
    
    print(f"Analysis for {react_name} saved to {output_file}")

def main(project_name, repo_creation_date):
    # Get the current working directory as the base project path
    project_path = os.getcwd()
    
    pr_csv = os.path.join(project_path, "github_api", project_name, "pr.csv")
    commit_csv = os.path.join(project_path, "pydrillerCSV", project_name, f"{project_name}_commit_data.csv")
    contrib_md = os.path.join(project_path, "github_api", project_name, "CONTRIBUTING.md")

    analyze_react_14(pr_csv)
    analyze_react_62(commit_csv, repo_creation_date)
    analyze_react_81(commit_csv)
    analyze_react_9(contrib_md)
    analyze_react_19(contrib_md)
    analyze_react_33(contrib_md)
    analyze_react_84(contrib_md)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:python3 AnalyserScripts/analyse_githubapi_data.py <project_name> <repo_creation_date>")
        sys.exit(1)
    
    project_name = sys.argv[1]
    repo_creation_date = sys.argv[2]
    main(project_name, repo_creation_date)
