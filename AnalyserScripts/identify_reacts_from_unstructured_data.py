import os

from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

reacts = {
    "ReACT-17": "Encourage mentors to collaborate with mentees on addressing bugs or issues.",
    "ReACT-27": "As a newcomer, explain what you've tried when asking for help, and use the provided template. (good-first-issue)",
    "ReACT-58": "Encourage senior developers to answer questions of newcomers",
    "ReACT-61": "Make the tasks technically interesting",
    "ReACT-67": "Clearly communicate unresolved issues to the developers",
    "ReACT-86": "Acknowledge all contributions of newcomers (comments)",
    "ReACT-95": "Set expectations and needs early: Show newcomers what is expected from them, where the difficulties lie, and what skills and level of expertise they need to have (what programming languages and technologies are used by the project, etc.). Place this information somewhere that newcomers access early in their journey (check issue comments under: Issue tag: “good first issue”)",
    "ReACT-103": "Keep the community informed about decisions."
}

my_file = client.files.upload(file='../github_api/kvrocks/issue_comments.txt')

with open("react_analysis_2.csv", "w") as f:
    for react in reacts:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                "Analyze the issue comments of a GitHub project and tell me in one word either yes or no if the project follows this recommendation: " + reacts[react],
                my_file
            ]
        )
        print(react, reacts[react], response.text)
        f.write(react + "," + reacts[react] + "," + response.text + "\n")
        
