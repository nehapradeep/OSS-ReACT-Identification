import pandas as pd
import csv
import os

def save_analysis(react_name, outcome, recommendation, output_file):
    with open(output_file, mode="a", encoding="utf-8", newline="") as csv_file:
        fieldnames = ["Project Name", "ReACT Name/Number", "Outcome", "Recommendation"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not os.path.isfile(output_file) or os.stat(output_file).st_size == 0:
            writer.writeheader()
        writer.writerow({
            "Project Name": 'kvrocks',
            "ReACT Name/Number": react_name,
            "Outcome": outcome,
            "Recommendation": recommendation
        })
    
    print(f"Analysis for {react_name} saved to {output_file}")

df = pd.read_csv('pydrillerCSV/kvrocks/kvrocks_commit_data.csv')
print(df.head())

# purva
def analyze_react_63(df):
    df['new_files_in_commit'] = df['Added Lines'] > 0
    average_modified_files = df['Number of Modified Files'].mean()
    average_new_files = df['new_files_in_commit'].sum()
    total_commits = len(df)
    modified_to_new_ratio = average_modified_files / average_new_files if average_new_files > 0 else 0

    outcome = f"Average modified-to-added lines ratio: {modified_to_new_ratio:.2f}. " \
              f"Average number of modified files per commit: {average_modified_files:.2f}. " \
              f"Average number of new files added: {average_new_files:.2f}. " \
              f"Total number of commits analyzed: {total_commits}."

    if modified_to_new_ratio > 2:
        recommendation = "No"
    else:
        recommendation = "Yes"

    return outcome, recommendation

# purva
def analyze_react_64(df):
    code_extensions = [
        '.cpp', '.cc', '.py', '.js', '.java', '.go', '.rb', '.php', '.cs', 
        '.sh', '.cmake', '.yaml', '.yml', '.h', '.c', '.m', '.swift', 
        '.rs', '.ts', '.tsx', '.pl', '.scala', '.lua', '.dart', '.ps1', '.bat',
        '.tcl', '.mod', '.sum', '.toml', '.in', '.clang-tidy', '.service'
    ]
    doc_extensions = [
        '.md', '.txt', '.rst', '.org', '.asciidoc', '.html', '.pdf', 
        '.ppt', '.docx', '.xls', '.csv', '.json', '.conf'
    ]
    
    code_files_without_extension = ['makefile', 'dockerfile', 'gitignore', 'gitmodules']
    doc_files_without_extension = ['readme', 'contributing', 'changelog', 'license', 'notice']

    df['File Extension'] = df['File Extension'].fillna('').str.strip().str.lower()
    df['File Name Lower'] = df['File Name'].str.lower()

    df['is_code_file'] = df.apply(lambda row: 
        row['File Extension'] in code_extensions or 
        (row['File Extension'] == '' and row['File Name Lower'] in code_files_without_extension), 
        axis=1
    )
    df['is_documentation_file'] = df.apply(lambda row:
        row['File Extension'] in doc_extensions or
        (row['File Extension'] == '' and row['File Name Lower'] in doc_files_without_extension),
        axis=1
    )

    code_file_count = df['is_code_file'].sum()
    doc_file_count = df['is_documentation_file'].sum()

    code_to_doc_ratio = code_file_count / doc_file_count if doc_file_count > 0 else float('inf')

    outcome = f"Number of code files modified: {code_file_count}. " \
              f"Number of documentation files modified: {doc_file_count}. " \
              f"Code-to-Documentation file ratio: {code_to_doc_ratio:.2f}."

    if code_to_doc_ratio > 2:
        recommendation = "No"
    else:
        recommendation = "Yes"

    return outcome, recommendation

# purva
def analyze_react_78(df):
    comment_updates_count = 0
    total_commits = len(df)
    
    for index, row in df.iterrows():
        if 'comment' in row['Commit Message'].lower():
            comment_updates_count += 1

    percentage_comment_updates = (comment_updates_count / total_commits) * 100 if total_commits > 0 else 0

    outcome = f"Total number of commits analyzed: {total_commits}. " \
              f"Number of commits involving code comment updates: {comment_updates_count}. " \
              f"Percentage of commits with comment updates: {percentage_comment_updates:.2f}%. "

    if percentage_comment_updates < 30:
        recommendation = "No"
    else:
        recommendation = "Yes"

    return outcome, recommendation
output_file = 'final_react_analysis.csv'
outcome_react63, recommendation_react63 = analyze_react_63(df)
save_analysis("ReACT-63", outcome_react63, recommendation_react63, output_file)
outcome_react64, recommendation_react64 = analyze_react_64(df)
save_analysis("ReACT-64", outcome_react64, recommendation_react64, output_file)
outcome_react78, recommendation_react78 = analyze_react_78(df)
save_analysis("ReACT-78", outcome_react78, recommendation_react78, output_file)
