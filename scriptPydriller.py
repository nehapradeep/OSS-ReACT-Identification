import csv
from pydriller import Repository

# Define the repository URL
repo_url = "https://github.com/apache/incubator-liminal.git"

# Define the CSV file name
csv_filename = "liminal_commit_data.csv"

# Open CSV file for writing
with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
    fieldnames = [
        "Commit Hash", "Author", "Author Email", "Author Date",
        "Committer", "Committer Email", "Committer Date",
        "Commit Message", "Branches", "In Main Branch", "Is Merge Commit",
        "Parents", "Number of Modified Files", "Insertions", "Deletions",
        "Lines Changed", "File Name", "File Extension", "Change Type",
        "Old Path", "New Path", "Added Lines", "Deleted Lines", "Total Lines Changed",
        "Readme Source Code"
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    # Traverse the repository commits
    for commit in Repository(repo_url).traverse_commits():
        for file in commit.modified_files:
            readme_content = ""  # Default: No README content unless it's a README file
            
            # Check if the file is a README file
            if file.filename.lower().startswith("readme"):
                readme_content = file.source_code[:500] if file.source_code else "No content"

            # Write commit and file details to CSV
            writer.writerow({
                "Commit Hash": commit.hash,
                "Author": commit.author.name,
                "Author Email": commit.author.email,
                "Author Date": commit.author_date,
                "Committer": commit.committer.name,
                "Committer Email": commit.committer.email,
                "Committer Date": commit.committer_date,
                "Commit Message": commit.msg,
                "Branches": ", ".join(commit.branches),
                "In Main Branch": commit.in_main_branch,
                "Is Merge Commit": commit.merge,
                "Parents": ", ".join(commit.parents),
                "Number of Modified Files": len(commit.modified_files),
                "Insertions": commit.insertions,
                "Deletions": commit.deletions,
                "Lines Changed": commit.lines,
                "File Name": file.filename,
                "File Extension": file.filename.split('.')[-1] if '.' in file.filename else "None",
                "Change Type": file.change_type,
                "Old Path": file.old_path if file.old_path else "N/A",
                "New Path": file.new_path if file.new_path else "N/A",
                "Added Lines": file.added_lines,
                "Deleted Lines": file.deleted_lines,
                "Total Lines Changed": file.added_lines + file.deleted_lines,
                "Readme Source Code": readme_content
            })

print(f"Data successfully saved in {csv_filename}")
