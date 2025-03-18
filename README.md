# OSS-ReACT-Identification

## Overview
This repository contains the implementation of our framework for analyzing the adoption of Researched Actionable Recommendations (ReACTs) in Open Source Software (OSS) projects. The framework applies automated techniques to extract sustainability-related insights from OSS repositories, assesses the accuracy of detection methods, and identifies commonly implemented best practices.

## Features
- Automated extraction of implemented Actionable Recommendations (ReACTS from OSS repositories.
- Analysis of structured and unstructured repository metadata.
- Manual validation to assess false positives and false negatives.
- Identification of frequently implemented sustainability recommendations.

## Dataset
Our analysis focuses on two main groups of OSS projects:

### Incubator Projects
- **ResilientDB**: A resilient database solution.
- **Celeborn**: Enhances data storage and processing efficiency.

### Graduated Projects
- **Kv Rocks**: A key-value store compatible with Redis protocols.
- **OpenDAL**: An Open Data Access Layer enabling seamless interaction with diverse storage services.
- **Pygwalker**: A Python library for exploratory data analysis with visualization.

Additionally, we expanded our dataset to include the ten most popular projects from the Apache Incubator, selected based on GitHub star ratings and metadata completeness:
- **SkyWalking**
- **RocketMQ**
- **Seata**
- **Spark**
- **Dubbo**
- **Superset**
- **ECharts**
- **Airflow**
- **Pulsar**
- **DolphinScheduler**

## Methodology
1. **Data Collection**: Extract repository metadata using GitHub API.
2. **Automated Detection**: Apply natural language processing (NLP) and rule-based methods to detect ReACT adoption.
3. **Manual Validation**: Assess accuracy by measuring false positives and false negatives.
4. **Trend Analysis**: Identify commonly adopted sustainability best practices.

## Installation & Usage
### Prerequisites
- Python 3.8+
- Required libraries listed in `requirements.txt`

### Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/nehapradeep/OSS-ReACT-Identification.git
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the analysis:
   ```sh
   ./reactAnalysis.sh <project_name> <repo_creation_timestamp>
   ```

## Results
The output includes:
- Extracted sustainability recommendations per project.
- Accuracy metrics (false positives, false negatives).
- Comparative trends in OSS project sustainability.

## Contributors
- Neha Pradeep
- Pranav Vinayak Wagh
- Purva Suhas Khadke
- Rajaram Manohar Joshi
- Vibha Govind Hegde
