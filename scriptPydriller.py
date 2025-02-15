import csv
import os
from pydriller import Repository

# Define the repository URL
repo_url = "https://github.com/apache/incubator-liminal.git"

# Define the CSV file name
csv_filename = "liminal_commit_data.csv"
readme_filename = "readme-liminal.md"
license_filename = "license-liminal.txt"
contributing_filename = "contributing-liminal.md"

# Initialize variables to store latest README, LICENSE, and CONTRIBUTING.md content
latest_readme = None
latest_license = None
latest_contributing = None

# Open CSV file for writing
with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
    fieldnames = [
        "Commit Hash", "Author Email", "Author Date", "Committer Email", "Committer Date",
        "Commit Message", "Branches", "In Main Branch", "Is Merge Commit",
        "Number of Modified Files", "File Name", "File Extension", "Change Type",
        "Added Lines", "Deleted Lines", "Total Lines Changed"
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    main_branches = {'main', 'master'}

    # Traverse the repository commits
    for commit in Repository(repo_url).traverse_commits():
        if not main_branches.intersection(commit.branches):
            continue
        
        for file in commit.modified_files:
            # Check if the file is a README file
            # if file.filename.lower().startswith("readme"):
            #     latest_readme = file.source_code if file.source_code else "No content"
            
            # Check if the file is a LICENSE file
            if file.filename.lower() == "license" or file.filename.lower().startswith("license"):
                latest_license = file.source_code if file.source_code else "No content"
            
            # Check if the file is a CONTRIBUTING.md file
            if file.filename.lower() == "contributing.md":
                latest_contributing = file.source_code if file.source_code else "No content"
            
            # Write commit and file details to CSV
            writer.writerow({
                "Commit Hash": commit.hash,
                "Author Email": commit.author.email,
                "Author Date": commit.author_date,
                "Committer Email": commit.committer.email,
                "Committer Date": commit.committer_date,
                "Commit Message": commit.msg,
                "Branches": ", ".join(commit.branches),
                "In Main Branch": commit.in_main_branch,
                "Is Merge Commit": commit.merge,
                "Number of Modified Files": len(commit.modified_files),
                "File Name": file.filename,
                "File Extension": file.filename.split('.')[-1] if '.' in file.filename else "None",
                "Change Type": file.change_type,
                "Added Lines": file.added_lines,
                "Deleted Lines": file.deleted_lines,
                "Total Lines Changed": file.added_lines + file.deleted_lines
            })

# Save the latest README, LICENSE, and CONTRIBUTING.md files
if latest_readme:
    with open(readme_filename, "w", encoding="utf-8") as f:
        f.write(latest_readme)

if latest_license:
    with open(license_filename, "w", encoding="utf-8") as f:
        f.write(latest_license)

if latest_contributing:
    with open(contributing_filename, "w", encoding="utf-8") as f:
        f.write(latest_contributing)

print(f"Data successfully saved in {csv_filename}")
print(f"Latest README saved in {readme_filename}")
print(f"Latest LICENSE saved in {license_filename}")
print(f"Latest CONTRIBUTING.md saved in {contributing_filename}")


