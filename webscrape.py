from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta, datetime
import requests
from bs4 import BeautifulSoup
import subprocess  # Needed to run shell commands

# Define the default arguments for the DAG
default_args = {
    'owner': 'airflow-demo',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retry_delay': timedelta(minutes=5),
}

# Initialize the DAG
dag = DAG(
    'web_scraping_and_data_versioning_dag',
    default_args=default_args,
    description='A simple web scraping DAG with selective data versioning',
    schedule_interval=timedelta(days=1),  # This schedules the DAG to run once every day
)

# Define the extract task
def extract():
    urls = ["https://www.dawn.com/", "https://www.bbc.com/"]
    all_links = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [link.get('href') for link in soup.find_all('a') if link.get('href') is not None]
            all_links.extend(links)
        else:
            print(f"Failed to retrieve {url}")
    return all_links

# Define the transform task
def transform(**kwargs):
    ti = kwargs['ti']
    extracted_data = ti.xcom_pull(task_ids='extract')
    transformed_data = []
    for url in extracted_data:
        # Example transformation: removing URL fragments and query parameters
        clean_url = url.split('#')[0].split('?')[0]
        transformed_data.append(clean_url)
    return transformed_data

# Define the load task
def load(**kwargs):
    ti = kwargs['ti']
    transformed_data = ti.xcom_pull(task_ids='transform')
    with open('/mnt/c/Users/hamma/OneDrive/Desktop/MLOpsA2/scraped.txt', 'w') as file:
        for url in transformed_data:
            file.write(url + '\n')
    print("Data saved to scraped.txt")

# Define the task to track changes with DVC
def dvc_add():
    subprocess.run(["dvc", "add", "scraped.txt"], check=True)
    print("Data tracked with DVC")

# Define the task to commit and push the DVC file hash to GitHub
def git_commit_push():
    subprocess.run(["git", "add", "scraped.txt.dvc"], check=True)  # Only add the .dvc file
    subprocess.run(["git", "commit", "-m", "Update DVC files"], check=True)
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("DVC file hash pushed to GitHub")

# Define the task to push data to DVC remote
def dvc_push():
    subprocess.run(["dvc", "commit"], check=True)
    subprocess.run(["dvc", "push"], check=True)
    print("Data pushed to DVC remote")

# Task operators
extract_task = PythonOperator(
    task_id='extract',
    python_callable=extract,
    dag=dag,
)

transform_task = PythonOperator(
    task_id='transform',
    python_callable=transform,
    provide_context=True,
    dag=dag,
)

load_task = PythonOperator(
    task_id='load',
    python_callable=load,
    provide_context=True,
    dag=dag,
)

dvc_add_task = PythonOperator(
    task_id='dvc_add',
    python_callable=dvc_add,
    dag=dag,
)

dvc_push_task = PythonOperator(
    task_id='dvc_push',
    python_callable=dvc_push,
    dag=dag,
)

git_commit_push_task = PythonOperator(
    task_id='git_commit_push',
    python_callable=git_commit_push,
    dag=dag,
)

# Setting task dependencies
extract_task >> transform_task >> load_task >> dvc_add_task >> dvc_push_task >> git_commit_push_task
