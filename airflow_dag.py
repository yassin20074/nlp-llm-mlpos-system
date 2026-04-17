'''Install the required libraries'''
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from ml.drift import run_drift
import mlflow

# create a function to check drift
def check_drift():
    drift = run_drift()
    print("Drift:", drift)
    return drift
# for exaple retrain model
def retrain_model():
    with mlflow.start_run():
        mlflow.log_param("retrained", True)
        mlflow.log_metric("status", 1)
        print("Model retrained (placeholder)")

def decision(**context):
    ti = context["ti"]
    drift = ti.xcom_pull(task_ids="check_drift")

    if drift:
        print("🚨 Drift detected → Retraining triggered")
        retrain_model()
    else:
        print("✅ No drift")
      
'''create a shedule dag'''

default_args = {
    "start_date": datetime(2024, 1, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="nlp_mlops_pipeline",
    schedule_interval="*/15 * * * *",
    catchup=False,
    default_args=default_args
) as dag:

    t1 = PythonOperator(
        task_id="check_drift",
        python_callable=check_drift
    )

    t2 = PythonOperator(
        task_id="decision",
        python_callable=decision,
        provide_context=True
    )

    t1 >> t2
