# Run example: ./windowsReactAnalysis.ps1 rocketmq 2016-11-30T08:00:08Z

param (
    [string]$ProjectName,
    [string]$RepoCreationDate
)

if (-not $ProjectName -or -not $RepoCreationDate) {
    Write-Host "Usage: ./run_analysis.ps1 <project_name> <repo_creation_date>"
    exit 1
}

# Run the scripts sequentially
python github_api/txt_csv.py $ProjectName
python AnalyserScripts/analyse_githubapi_data.py $ProjectName $RepoCreationDate
python AnalyserScripts/analyseReACTs.py $ProjectName
python AnalyserScripts/readme.py $ProjectName