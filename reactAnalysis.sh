#!/bin/bash
# Run example : ./run_analysis.sh rocketmq 2016-11-30T08:00:08Z

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <project_name> <repo_creation_date>"
    exit 1
fi


PROJECT_NAME=$1
REPO_CREATION_DATE=$2

# Run the scripts sequentially
python github_api/txt_csv.py "$PROJECT_NAME"
python3 AnalyserScripts/analyse_githubapi_data.py "$PROJECT_NAME" "$REPO_CREATION_DATE"
python3 AnalyserScripts/analyseReACTs.py "$PROJECT_NAME"
python3 AnalyserScripts/readme.py "$PROJECT_NAME"
