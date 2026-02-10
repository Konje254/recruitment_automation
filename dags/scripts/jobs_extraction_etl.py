import os
import pandas as pd
import requests
from pathlib import Path


def run_remotive_etl():
    # API endpoint that returns remote job listings in JSON format
    api = "https://remotive.com/api/remote-jobs"

    # Path to the CSV file where jobs will be stored
    AIRFLOW_HOME = Path(os.environ["AIRFLOW_HOME"])
    PROJECT_ROOT = AIRFLOW_HOME.parent
    csv_file = PROJECT_ROOT/'data'/"jobs.csv"

    # Send request to the API
    response = requests.get(api)

    # Convert JSON response to a Python dictionary
    data = response.json()

    # Extract the list of jobs from the response
    jobs = data["jobs"]

    # Convert jobs list into a pandas DataFrame
    df = pd.DataFrame(jobs)

    # Select only the columns we want to store in the CSV
    df = df[
        [
            "id",
            "title",
            "company_name",
            "category",
            "job_type",
            "candidate_required_location",
            "salary",
            "publication_date",
            "url",
            "tags",
        ]
    ]

    # Convert tags from list format to a comma-separated string
    df["tags"] = df["tags"].apply(
        lambda x: ", ".join(x) if isinstance(x, list) else ""
    )

    # If the CSV already exists, load it and append new data
    if csv_file.exists():
        old_df = pd.read_csv(csv_file)
        df = pd.concat([old_df, df], ignore_index=True)

    # Remove duplicate records based on id, title, and company_name
    # Keep the most recent version of each job
    df = df.drop_duplicates(
        subset=["id", "title", "company_name"],
        keep="last"
    )

    # Save the cleaned and updated data back to CSV
    df.to_csv(csv_file, index=False, encoding="utf-8-sig")
