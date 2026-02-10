# recruitment_auto (Airflow + Job Scraping)

A local Apache Airflow learning project that schedules a daily job-scraping ETL.  
Current source: **Remotive Jobs API** → cleans/deduplicates → writes to `data/jobs.csv`.

## What this project demonstrates
- Writing an Airflow **DAG** with a **PythonOperator**
- Local Airflow setup with a project-scoped `AIRFLOW_HOME`
- Scheduling + manual triggering from the Airflow UI
- Basic ETL patterns: extract → transform → load (CSV)

## Project structure (important parts)
```text
recruitment_auto/
  airflow/
    dags/
      jobs_extraction_dag.py
      scripts/
        jobs_extraction_etl.py
  data/
    jobs.csv
```

## Prerequisites
- Python 3.10+ (this repo uses 3.12)
- pip / venv

## Setup (first time)
```bash
cd recruitment_auto
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

export AIRFLOW_HOME="$(pwd)/airflow"
export AIRFLOW__CORE__DAGS_FOLDER="$AIRFLOW_HOME/dags"
export AIRFLOW__CORE__LOAD_EXAMPLES=False

airflow db migrate
```

## Run Airflow locally
```bash
cd recruitment_auto
source venv/bin/activate
export AIRFLOW_HOME="$(pwd)/airflow"
export AIRFLOW__CORE__DAGS_FOLDER="$AIRFLOW_HOME/dags"
export AIRFLOW__CORE__LOAD_EXAMPLES=False

airflow standalone
```

Open the UI: `http://localhost:8080`  
(Standalone prints the username/password to your terminal the first time.)

## How scheduling works here
In `airflow/dags/jobs_extraction_dag.py`:
- DAG id: `remotive_jobs_etl`
- schedule: `timedelta(days=1)` (daily)
- task: `run_remotive_etl` calls `run_remotive_etl()` from `scripts/jobs_extraction_etl.py`

### Change the schedule
Example: daily at 06:00
```python
schedule = "0 6 * * *"
```

## Output
- CSV: `data/jobs.csv`
- Logs: `airflow/logs/`

## Troubleshooting quick checks
### 1) Confirm paths Airflow is using
```bash
airflow info | egrep -i "airflow_home|dags_folder|sql_alchemy_conn|plugins_folder|base_log_folder"
```

### 2) Bypass Airflow and test import
```bash
python airflow/dags/jobs_extraction_dag.py
```

### 3) Watch DAG parsing
```bash
airflow dag-processor
```

## Recommended .gitignore
Do **not** commit local Airflow state:
```gitignore
# Airflow local state (generated)
airflow/airflow.db*
airflow/logs/
airflow/plugins/
airflow/airflow.cfg

# Python
__pycache__/
*.pyc
venv/
.env
```

