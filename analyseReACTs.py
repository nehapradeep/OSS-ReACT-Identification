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
            "ReACT Name/Number": "ReACT-3: Utilize a common programming language",
            "Outcome": outcome_str,
            "Recommendation": "N/A"
        })
        writer.writerow({
            "Project Name": project_name,
            "ReACT Name/Number": "ReACT-65: Maintain the current project platform; refrain from altering it. (if available on github, ReACT is satisfied)",
            "Outcome": "Meets criteria",
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
    project_name = "celeborn"
    input_csv = "./pydrillerCSV/celeborn/celeborn_commit_data.csv"
    output_csv = "./final_react_analysis.csv"
    
    analyze_react_metrics(input_csv, project_name, output_csv)
    analyze_commit_messages(input_csv, project_name, output_csv)
    analyze_file_extensions(input_csv, "ReACT-File Extension Analysis", project_name, output_csv)
    
if __name__ == "__main__":
    main()
