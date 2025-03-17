import csv
import os
from datetime import datetime, timedelta, timezone
from pydriller import Repository

# Define the repository URL
repo_url = "https://github.com/apache/echarts"

# Define the time window (last 1 year)
one_year_ago = datetime.now(timezone.utc) - timedelta(days=180)

# Define file paths
csv_filename = "pydrillerCSV/echarts/echarts_commit_data_2.csv"
readme_filename = "pydrillerCSV/echarts/readme-echarts.md"
license_filename = "pydrillerCSV/echarts/license-echarts.txt"
contributing_filename = "pydrillerCSV/echarts/contributing-echarts.md"

# Create necessary directories
os.makedirs(os.path.dirname(csv_filename), exist_ok=True)

print(f"Fetching latest commits from {repo_url} (last 1 year)...")

# Open CSV file for writing
with open(csv_filename, mode="w", newline="", encoding="utf-8") as csv_file:
    fieldnames = [
        "Commit Hash", "Author Email", "Author Date", "Committer Email", "Committer Date",
        "Commit Message", "In Main Branch", "Is Merge Commit",
        "Number of Modified Files", "File Name", "File Extension",
        "Added Lines", "Deleted Lines", "Total Lines Changed"
    ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    latest_readme = None
    latest_license = None
    latest_contributing = None
    commit_count = 0
    skipped_commits = 0  # Track skipped commits

    # Traverse commits directly from latest to oldest
    for commit in Repository(repo_url, since=one_year_ago, order="reverse").traverse_commits():
        try:
            commit_count += 1
            print(f"Processing Commit: {commit.hash} | Date: {commit.author_date}")

            for file in commit.modified_files:
                # Skip binary and object files
                if file.filename.endswith(('.o', '.obj', '.d', '.exe', '.bin', '.dll', '.so', '.class', '.jar')) or file.source_code is None:
                    continue

                # Store latest README.md content
                if file.filename.lower() == "readme.md":
                    latest_readme = file.source_code if file.source_code else "No content"

                # Store latest LICENSE content
                if file.filename.lower() == "license" or file.filename.lower().startswith("license"):
                    latest_license = file.source_code if file.source_code else "No content"

                # Store latest CONTRIBUTING.md content
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
                    "In Main Branch": commit.in_main_branch,
                    "Is Merge Commit": commit.merge,
                    "Number of Modified Files": len(commit.modified_files),
                    "File Name": file.filename,
                    "File Extension": file.filename.split('.')[-1] if '.' in file.filename else "None",
                    "Added Lines": file.added_lines,
                    "Deleted Lines": file.deleted_lines,
                    "Total Lines Changed": file.added_lines + file.deleted_lines
                })

        except Exception as e:
            skipped_commits += 1
            print(f"Skipping commit {commit.hash} due to error: {e}")

    print(f"Completed! Processed {commit_count} commits, skipped {skipped_commits} problematic commits.")

# Save latest README, LICENSE, and CONTRIBUTING.md files
def save_file(content, filename, filetype):
    if content:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Saved latest {filetype} in {filename}")

save_file(latest_readme, readme_filename, "README")
save_file(latest_license, license_filename, "LICENSE")
save_file(latest_contributing, contributing_filename, "CONTRIBUTING.md")

print(f"All data saved successfully in {csv_filename}")
