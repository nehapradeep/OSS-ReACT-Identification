import re
import os
import sys


# def save_analysis(react_code, outcome, recommendation, output_file):
#     with open(output_file, mode='a', encoding='utf-8') as file:
#         file.write(f"{react_code},{outcome},{recommendation}\n")
def save_analysis(react_name, outcome, recommendation, output_file, project_name):
    file_exists = os.path.isfile(output_file)
    with open(output_file, mode="a", encoding="utf-8") as md_file:
        if not file_exists or os.stat(output_file).st_size == 0:
            md_file.write("Project Name,ReACT Name/Number,Outcome,Recommendation\n")        
        md_file.write(f"{project_name},{react_name},{outcome},{recommendation}\n")
    
    print(f"Analysis for {react_name} saved to {output_file}")


def analyze_react_100(readme_content, output_file, project_name):
    documentation_keywords = ["document", "process", "practice", "documentation"]
    documentation_found = any(keyword in readme_content.lower() for keyword in documentation_keywords)
    
    if documentation_found:
        outcome = "Processes and practices are documented within the project."
        recommendation = "Yes"
    else:
        outcome = "No documentation of processes and practices found in the project."
        recommendation = "No"
    
    save_analysis("ReACT-100", outcome, recommendation, output_file, project_name)


def analyze_react_93(readme_content, output_file, project_name):
    zulip_found = "zulip" in readme_content.lower()
    mailing_list_found = "mailing list" in readme_content.lower()

    if zulip_found and mailing_list_found:
        outcome = "Zulip chat and Mailing List are both available as communication channels."
        recommendation = "Yes"
    elif zulip_found:
        outcome = "Zulip chat is available as a communication channel."
        recommendation = "Yes"
    elif mailing_list_found:
        outcome = "A Mailing List is available for communication."
        recommendation = "Yes"
    else:
        outcome = "No clear communication channels (like Zulip or chat platforms) found."
        recommendation = "No"
    
    save_analysis("ReACT-93", outcome, recommendation, output_file, project_name)


def analyze_react_77(readme_content, output_file, project_name):
    mailing_list_found = "mailing list" in readme_content.lower()
    mailing_list_encouraged = bool(re.search(r"(subscribe|join the mailing list)", readme_content, re.IGNORECASE))

    if mailing_list_found and mailing_list_encouraged:
        outcome = "Mailing list is mentioned and encouraged."
        recommendation = "Yes"
    elif mailing_list_found:
        outcome = "Mailing list is mentioned, but not encouraged."
        recommendation = "No"
    else:
        outcome = "Mailing list is not mentioned."
        recommendation = "No"
    
    save_analysis("ReACT-77", outcome, recommendation, output_file, project_name)


def analyze_react_60(readme_content, output_file, project_name):
    stars_found = "github stars" in readme_content.lower()
    social_media_links_found = any(link in readme_content.lower() for link in ["twitter", "medium", "linkedin"])

    if stars_found and social_media_links_found:
        outcome = "GitHub stars and social media links are present."
        recommendation = "Yes"
    elif stars_found:
        outcome = "GitHub stars are present, but social media links are missing."
        recommendation = "No"
    else:
        outcome = "GitHub stars are not present."
        recommendation = "No"
    
    save_analysis("ReACT-60", outcome, recommendation, output_file, project_name)


def analyze_react_53(readme_content, output_file, project_name):
    incubated_found = "apache software foundation" in readme_content.lower()

    if incubated_found:
        outcome = "The project is incubated by the Apache Software Foundation."
        recommendation = "Yes"
    else:
        outcome = "The project is not incubated by a large software foundation."
        recommendation = "No"
    
    save_analysis("ReACT-53", outcome, recommendation, output_file, project_name)


def analyze_react_20(readme_content, output_file, project_name):
    communication_channels = []
    if "zulip" in readme_content.lower():
        communication_channels.append("Zulip")
    if "discord" in readme_content.lower():
        communication_channels.append("Discord")
    if "mailing list" in readme_content.lower():
        communication_channels.append("Mailing List")
    if "Slack" in readme_content.lower():
        communication_channels.append("slack")
    if "twitter" in readme_content.lower() or "x" in readme_content.lower():
        communication_channels.append("Twitter")
    if "wechat" in readme_content.lower():
        communication_channels.append("WeChat")

    if len(set(communication_channels)) >= 2:
        outcome = f"The project communicates through various channels: {', '.join(set(communication_channels))}."
        recommendation = "Yes"
    else:
        outcome = "The project does not communicate through various channels."
        recommendation = "No"
    
    save_analysis("ReACT-20", outcome, recommendation, output_file, project_name)


def analyze_react_97(readme_content, output_file, project_name):
    license_found = "apache license" in readme_content.lower()

    if license_found:
        outcome = "The project is licensed under the Apache License."
        recommendation = "Yes"
    else:
        outcome = "The project license is not mentioned or not Apache License."
        recommendation = "No"
    
    save_analysis("ReACT-97", outcome, recommendation, output_file, project_name)


def analyze_react_98(readme_content, output_file, project_name):
    build_instructions_found = any(keyword in readme_content.lower() for keyword in ["build", "run", "docker", "./x.py"])

    if build_instructions_found:
        outcome = "Clear build and run instructions are provided."
        recommendation = "Yes"
    else:
        outcome = "No clear build and run instructions are provided."
        recommendation = "No"
    
    save_analysis("ReACT-98", outcome, recommendation, output_file, project_name)


def analyze_react_95(readme_content, output_file, project_name):
    contribution_found = "contributing" in readme_content.lower()

    if contribution_found:
        outcome = "Contribution guidelines are clearly mentioned."
        recommendation = "Yes"
    else:
        outcome = "Contribution guidelines are not mentioned."
        recommendation = "No"
    
    save_analysis("ReACT-95", outcome, recommendation, output_file, project_name)


def analyze_react_102(readme_content, output_file, project_name):
    security_found = any(keyword in readme_content.lower() for keyword in ["security", "vulnerability", "secure", "security considerations"])

    if security_found:
        outcome = "Security considerations are documented."
        recommendation = "Yes"
    else:
        outcome = "Security considerations are not documented."
        recommendation = "No"
    
    save_analysis("ReACT-102", outcome, recommendation, output_file, project_name)

def main(project_name):
    readme_file = os.path.join("github_api", project_name, "README.md")
    output_file = "final_react_analysis.csv"
    
    with open(readme_file, "r", encoding="utf-8") as file:
        readme_content = file.read()
    
    analyze_react_100(readme_content, output_file, project_name)
    analyze_react_93(readme_content, output_file, project_name)
    analyze_react_77(readme_content, output_file, project_name)
    analyze_react_60(readme_content, output_file, project_name)
    analyze_react_53(readme_content, output_file, project_name)
    analyze_react_20(readme_content, output_file, project_name)
    analyze_react_97(readme_content, output_file, project_name)
    analyze_react_98(readme_content, output_file, project_name)
    analyze_react_95(readme_content, output_file, project_name)
    analyze_react_102(readme_content, output_file, project_name)
    
    print(f"Analysis completed. Results saved to {output_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <project_name>")
        sys.exit(1)
    
    project_name = sys.argv[1]
    main(project_name)
