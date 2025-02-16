import csv
import os
import pandas as pd

def analyze_react_metrics(csv_filename):
    project_metrics = {
        "ReACT-11 Keep the project small and simple.": True,  # Assume small and simple unless large LOC is detected
        "ReACT-26 Conduct unit tests.": False,  # Will be True if test files are found
        "ReACT-32 Promote code transparency. Keep the code as simple as possible": False,  # Will be evaluated based on comments
        "ReACT-82 Have and enforce a code of conduct": False   # Will be True if CODE_OF_CONDUCT.md exists
    }
    
    total_files = 0
    total_loc = 0
    total_comment_lines = 0
    test_files = 0
    
    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            total_files += 1
            total_loc += int(row["Total Lines Changed"])
            
            file_name = row["File Name"].lower()
            file_extension = row["File Extension"].lower()
            
            # Check for test files
            if "test" in file_name or file_name.startswith("test_"):
                test_files += 1
                
            # Check for code of conduct
            if file_name == "code_of_conduct.md":
                project_metrics["ReACT-82 Have and enforce a code of conduct (have file named CODE_OF_CONDUCT.md"] = True
                
            # Approximate comment ratio (assuming comments are 20% of deleted lines)
            total_comment_lines += int(row["Deleted Lines"]) * 0.2
    
    # Evaluate ReACT-11: Project simplicity (if LOC > 10,000, recommend keeping it simple) - Can be Vague
    if total_loc > 1000000:
        project_metrics["ReACT-11 Keep the project small and simple."] = False
    
    # Evaluate ReACT-26: If no test files exist, recommend unit tests
    if test_files > 0:
        project_metrics["ReACT-26 Conduct unit tests."] = True
    
    # Evaluate ReACT-32: If comments are less than 15% of total LOC, recommend more transparency
    if total_comment_lines / total_loc > 0.15:
        project_metrics["ReACT-32 Promote code transparency. Keep the code as simple as possible"] = True
    
    recommendations = [key for key, value in project_metrics.items() if not value]
    
    if recommendations:
        print("Recommendations:")
        for react in recommendations:
            print(f"- {react}")
    else:
        print("All ReACT guidelines are met! No recommendations needed.")


def analyze_file_extensions(file_path, react_number, project_name="Liminal Project", output_file="react_analysis_output.csv"):
    # Step 1: Read the project's CSV file
    df = pd.read_csv(file_path)
    
    # Step 2: Compute the percentage of each file extension
    extension_counts = df["File Extension"].value_counts()
    extension_percentage = (extension_counts / extension_counts.sum()) * 100
    
    # Step 3: Prepare the output CSV file
    file_exists = os.path.isfile(output_file)
    
    # Step 4: Store the results in a DataFrame
    outcome_str = "; ".join([f"{ext}: {perc:.2f}%" for ext, perc in extension_percentage.items()])
    
    output_data = pd.DataFrame({
        "OSS Project": [project_name],
        "ReACT number": [react_number],
        "Outcome": [outcome_str]  # Store all percentages in a single cell
    })
    
    # Step 5: Save or append to the CSV file
    output_data.to_csv(output_file, mode='a', index=False, header=not file_exists)
    
    print(f"Analysis saved to {output_file}")

def analyze_commit_messages(csv_filename):
    project_metrics = {"ReACT-66 Perform adequate testing before integrating a feature": False}
    total_commits = 0
    revert_commits = 0
    
    with open(csv_filename, mode="r", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            commit_message = row["Commit Message"].lower()
            total_commits += 1
            
            if "test" in commit_message or "tested" in commit_message or "unit test" in commit_message:
                project_metrics["ReACT-66 Perform adequate testing before integrating a feature"] = True
            
            if "revert" in commit_message:
                revert_commits += 1
    
    if total_commits > 0 and (revert_commits / total_commits) > 0.1:  # If more than 10% commits are revert commits
        project_metrics["ReACT-66 Perform adequate testing before integrating a feature"] = False
    
    recommendations = [key for key, value in project_metrics.items() if not value]
    
    if recommendations:
        print("Recommendations for commit messages:")
        for react in recommendations:
            print(f"- {react}")
    else:
        print("ReACT guidelines for ReACT 66 is met!")

def analyze_contributing_md(directory_path):
    project_metrics = {
        "ReACT-9 Grant newcomer access to the main repository": False,
        "ReACT-19 Flag newcomers to ensure a welcoming environment for them": False,
        "ReACT-33 Provide clear and detailed contribution guidelines": False,
        "ReACT-84 Provide onboarding support and help newcomers to make their first contribution": False
    }
    
    contributing_md_path = os.path.join(directory_path)
    if os.path.exists(contributing_md_path):
        with open(contributing_md_path, "r", encoding="utf-8") as f:
            content = f.read().lower()
            
            if "how to request for access" in content:
                project_metrics["ReACT-9 Grant newcomer access to the main repository"] = True
            if "flag newcomers" in content:
                project_metrics["ReACT-19 Flag newcomers to ensure a welcoming environment for them"] = True
            if "contribution guidelines" in content:
                project_metrics["ReACT-33 Provide clear and detailed contribution guidelines"] = True
            if "onboarding support" in content or "first contribution" in content:
                project_metrics["ReACT-84 Provide onboarding support and help newcomers to make their first contribution"] = True
    
    recommendations = [key for key, value in project_metrics.items() if not value]
    
    if recommendations:
        print("Recommendations [CONTRIBUTING.md]")
        for react in recommendations:
            print(f"- {react}")
    else:
        print("CONTRIBUTING.md are met!")

# Example usage
file_path = "liminal_commit_data.csv"
react_number = "ReACT-3"
analyze_file_extensions(file_path, react_number)

csv_filename = "liminal_commit_data.csv"
analyze_react_metrics(csv_filename)
directory_path = "contributing-liminal.md"
analyze_contributing_md(directory_path)
analyze_commit_messages(csv_filename)

def analyze_react_16(file_path, output_file="react_commit_author.csv"):
    """
    Analyze ReACT-16: Identify the number of integrators (committers who merged pull requests)
    and track their expansion over time.
    """
    df = pd.read_csv(file_path)
    print("Column Names:", df.columns.tolist())  

    df.columns = df.columns.str.strip()  # Removes spaces from column names
    if "Commit Message" not in df.columns:
        print("Error: 'Commit Message' column not found in CSV.")
        return
    merge_commits = df[df["Commit Message"].str.contains("Merge", case=False, na=False)]

    unique_integrators = merge_commits["Committer Email"].nunique()
    total_merges = merge_commits.shape[0]

    unique_committer_emails = merge_commits["Committer Email"].unique()

    if not merge_commits.empty:
        earliest_merge = merge_commits["Committer Date"].min()
        latest_merge = merge_commits["Committer Date"].max()
    else:
        earliest_merge = latest_merge = "No merge commits found"

    file_exists = os.path.isfile(output_file)
    output_data = pd.DataFrame({
        "OSS Project": ["Celeborn"],
        "ReACT number": ["ReACT-16"],
        "Total Integrators": [unique_integrators],
        "Total Merge Commits": [total_merges],
        "Earliest Merge Date": [earliest_merge],
        "Latest Merge Date": [latest_merge],
        "Unique Committer Emails": [", ".join(unique_committer_emails)]
    })

    output_data.to_csv(output_file, mode='a', index=False, header=not file_exists)
    print(f"ReACT-16 Analysis saved to {output_file}")

def analyze_react_36(file_path, output_file="react_36_analysis.csv"):
    """
    Analyze ReACT-36: Maintain a small number of core/active developers.
    """
    df = pd.read_csv(file_path)
    print("Column Names:", df.columns.tolist())  
    df.columns = df.columns.str.strip()  # Removes spaces from column names
    if "Author Email" not in df.columns or "Committer Date" not in df.columns:
        print("Error: Required columns ('Author Email', 'Committer Date') not found in CSV.")
        return

    total_commits = df.shape[0]
    commits_per_author = df["Author Email"].value_counts()
    commit_percentages = (commits_per_author / total_commits) * 100
    author_timelines = {}
    for author in commits_per_author.index:
        author_commits = df[df["Author Email"] == author]
        first_commit = author_commits["Committer Date"].min()
        latest_commit = author_commits["Committer Date"].max()
        author_timelines[author] = (first_commit, latest_commit)

    file_exists = os.path.isfile(output_file)
    output_data = []
    for author, commit_percentage in commit_percentages.items():
        first_commit, latest_commit = author_timelines[author]
        output_data.append({
            "Author Email": author,
            "Commit Percentage": f"{commit_percentage:.2f}%",
            "First Commit Date": first_commit,
            "Latest Commit Date": latest_commit
        })

    output_df = pd.DataFrame(output_data)
    output_df.to_csv(output_file, mode='a', index=False, header=not file_exists)
    
    print(f"ReACT-36 Analysis saved to {output_file}")
    print(output_df)

def analyze_react_38_with_loc(file_path, min_commits=10, min_months_active=3, min_lines_of_code=1000, output_file="react_commit_author.csv"):
    """
    Analyze ReACT-38: Foster contributions from experienced contributors.
    Identify contributors who have been active for a significant amount of time,
    made a sufficient number of commits, and contributed a significant amount of lines.
    """
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()  # Removes spaces from column names
    if "Author Email" not in df.columns or "Committer Date" not in df.columns or "Total Lines Changed" not in df.columns:
        print("Error: Required columns ('Author Email', 'Committer Date', 'Total Lines Changed') not found in CSV.")
        return
    commits_per_author = df["Author Email"].value_counts()

    contributor_lines_of_code = df.groupby("Author Email")["Total Lines Changed"].sum()
    experienced_contributors = commits_per_author[commits_per_author >= min_commits]

    experienced_contributors = experienced_contributors[contributor_lines_of_code[experienced_contributors.index] >= min_lines_of_code]
    contributor_timelines = {}
    for author in experienced_contributors.index:
        author_commits = df[df["Author Email"] == author]
        
        first_commit = pd.to_datetime(author_commits["Committer Date"]).min()
        latest_commit = pd.to_datetime(author_commits["Committer Date"]).max()

        months_active = (latest_commit.year - first_commit.year) * 12 + (latest_commit.month - first_commit.month)
        
        if months_active >= min_months_active:
            contributor_timelines[author] = (commits_per_author[author], contributor_lines_of_code[author], first_commit, latest_commit)

    file_exists = os.path.isfile(output_file)

    output_data = []
    for author, (commit_count, total_lines, first_commit, latest_commit) in contributor_timelines.items():
        output_data.append({
            "Author Email": author,
            "Total Commits": commit_count,
            "Total Lines Contributed": total_lines,
            "First Commit Date": first_commit,
            "Latest Commit Date": latest_commit,
            "Months Active": (latest_commit.year - first_commit.year) * 12 + (latest_commit.month - first_commit.month)
        })

    output_df = pd.DataFrame(output_data)
    output_df.to_csv(output_file, mode='a', index=False, header=not file_exists)
    
    print(f"ReACT-38 Analysis saved to {output_file}")
    print(output_df)

# Example usage
file_path = "pydrillerCSV/celeborn_commit_data.csv"
react_number = "ReACT-16"
analyze_file_extensions(file_path, react_number)
analyze_react_16(file_path)
analyze_react_36(file_path)
analyze_react_38_with_loc(file_path)

csv_filename = "pydrillerCSV/celeborn_commit_data.csv"
analyze_react_metrics(csv_filename)
