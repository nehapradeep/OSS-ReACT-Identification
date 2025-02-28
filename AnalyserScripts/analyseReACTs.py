import csv
import os
import pandas as pd

def analyze_react_metrics(csv_filename, project_name, output_file="final_react_analysis.csv"):
    project_metrics = {
        "ReACT-11 Keep the project small and simple.": True,
        "ReACT-26 Conduct unit tests.": False,
        "ReACT-32 Promote code transparency. Keep the code as simple as possible": False,
        "ReACT-82 Have and enforce a code of conduct": False
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
            
            if "test" in file_name or file_name.startswith("test_"):
                test_files += 1
            
            if file_name == "code_of_conduct.md":
                project_metrics["ReACT-82 Have and enforce a code of conduct"] = True
            
            total_comment_lines += int(row["Deleted Lines"]) * 0.2
    
    # Analysis of ReACT-11
    if total_loc > 1000000:
        project_metrics["ReACT-11 Keep the project small and simple."] = False
    
    # Analysis of ReACT-26
    if test_files > 0:
        project_metrics["ReACT-26 Conduct unit tests."] = True
    
    # Analysis of ReACT-32
    if total_comment_lines / total_loc > 0.15:
        project_metrics["ReACT-32 Promote code transparency. Keep the code as simple as possible"] = True
    
    # Writing the results to the CSV
    with open(output_file, mode="a", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["Project Name", "ReACT Name/Number", "Outcome", "Recommendation"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not os.path.isfile(output_file) or os.stat(output_file).st_size == 0:
            writer.writeheader()
        
        for key in project_metrics:
            analysis = "Meets criteria"
            recommendation = "Recommend"
            if not project_metrics[key]:
                analysis = "Does not meet criteria"
                # Add specific explanation to Analysis
                if key == "ReACT-11 Keep the project small and simple.":
                    analysis += f" (Total LOC is {total_loc}, which exceeds the recommended limit of 1 million.)"
                elif key == "ReACT-26 Conduct unit tests.":
                    analysis += " (No unit tests found, but test files are present.)"
                elif key == "ReACT-32 Promote code transparency. Keep the code as simple as possible":
                    analysis += f" (Comment ratio is {total_comment_lines / total_loc:.2f}, which is below the recommended threshold of 15%.)"
                elif key == "ReACT-82 Have and enforce a code of conduct":
                    analysis += " (No code of conduct file found in the project.)"
                recommendation = "Do not recommend"
            
            writer.writerow({
                "Project Name": project_name,
                "ReACT Name/Number": key,
                "Outcome": analysis,
                "Recommendation": recommendation
            })
    
    print(f"Analysis saved to {output_file}")

def analyze_file_extensions(file_path, react_number, project_name, output_file="final_react_analysis.csv"):
    df = pd.read_csv(file_path)
    extension_counts = df["File Extension"].value_counts()
    extension_percentage = (extension_counts / extension_counts.sum()) * 100
    file_exists = os.path.isfile(output_file)
    outcome_str = "; ".join([f"{ext}: {perc:.2f}%" for ext, perc in extension_percentage.items()])
    
    with open(output_file, mode="a", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["Project Name", "ReACT Name/Number", "Outcome", "Recommendation"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not file_exists or os.stat(output_file).st_size == 0:
            writer.writeheader()
        
        writer.writerow({
            "Project Name": project_name,
            "ReACT Name/Number": react_number,
            "Outcome": outcome_str,
            "Recommendation": "N/A"
        })
    
    print(f"Analysis saved to {output_file}")

def analyze_commit_messages(csv_filename, project_name, output_file="final_react_analysis.csv"):
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
    
    if total_commits > 0 and (revert_commits / total_commits) > 0.1:
        project_metrics["ReACT-66 Perform adequate testing before integrating a feature"] = False
    
    with open(output_file, mode="a", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["Project Name", "ReACT Name/Number", "Outcome", "Recommendation"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not os.path.isfile(output_file) or os.stat(output_file).st_size == 0:
            writer.writeheader()
        
        for key in project_metrics:
            analysis = "Meets criteria"
            recommendation = "Recommend"
            if not project_metrics[key]:
                analysis = "Does not meet criteria"
                # Add specific explanation to Analysis
                if key == "ReACT-66 Perform adequate testing before integrating a feature":
                    analysis += " (More than 10% of commits are revert commits, indicating insufficient testing before integration.)"
                recommendation = "Do not recommend"
            
            writer.writerow({
                "Project Name": project_name,
                "ReACT Name/Number": key,
                "Outcome": analysis,
                "Recommendation": recommendation
            })
    
    print(f"Analysis saved to {output_file}")

def main():
    project_name = "ResDB"
    input_csv = "resdb_commit_data2.csv"
    output_csv = "final_react_analysis.csv"
    
    analyze_react_metrics(input_csv, project_name, output_csv)
    analyze_commit_messages(input_csv, project_name, output_csv)
    analyze_file_extensions(input_csv, "ReACT-File Extension Analysis", project_name, output_csv)
    file_path = "pydrillerCSV/celeborn_commit_data.csv"
    react_number = "ReACT-16"
    analyze_file_extensions(file_path, react_number)
    analyze_react_16(file_path)
    analyze_react_36(file_path)
    analyze_react_38_with_loc(file_path)

csv_filename = "pydrillerCSV/celeborn_commit_data.csv"
analyze_react_metrics(csv_filename)
    
if __name__ == "__main__":
    main()


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

