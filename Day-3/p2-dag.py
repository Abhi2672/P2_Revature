from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.hooks.gcs import GCSHook
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.microsoft.mssql.hooks.mssql import MsSqlHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
import pandas as pd
from google.cloud import storage
from google.cloud import bigquery

# Currency rates for conversion
CURRENCY_RATES = {
    "India": 1,        # INR
    "Japan": 0.57,     # JPY
    "Norway": 8.21,    # NOK
    "SriLanka": 0.25, # LKR
    "HongKong": 10.93, # HKD
    "Oman": 215.54,    # OMR
    "Germany": 89.34,  # EUR
    "Qatar": 22.87     # QAR
}


# GCS bucket names
GCS_BUCKET = "country_bucket"

# Database connections configuration
DB_CONNECTIONS = {
    "Oman": ("mysql_oman", "Oman_Sales"),
    "Norway": ("postgres_norway", "Norway_Sales"),
    "India": ("mssql_india", "India_Sales"),
    "Germany": ("mysql_germany", "Germany_Sales"),
    "Qatar": ("mysql_qatar", "Qatar_Sales")
}

def read_and_combine_data(**kwargs):
    # GCS - Read CSV, JSON, Excel files
    storage_client = storage.Client()
    files = {
        "csv": "Japan_Sales.csv",
        "json": "SriLanka_Sales.json",
        "xlsx": "HongKong_Sales.xlsx"
    }

    # Read the files from GCS into DataFrame
    dataframes = []
    for file_format, file_name in files.items():
        local_file = f"/tmp/{file_name}"

        # Download from GCS
        bucket = storage_client.bucket(GCS_BUCKET)
        blob = bucket.blob(file_name)
        blob.download_to_filename(local_file)

        # Load file into pandas dataframe
        if file_format == "csv":
            df = pd.read_csv(local_file)
            df["Country"]="Japan"
        elif file_format == "json":
            df = pd.read_json(local_file)
            df["Country"]="SriLanka"
        elif file_format == "xlsx":
            df = pd.read_excel(local_file)
            df["Country"]="HongKong"
        else:
            raise ValueError("Unsupported format")
        
        dataframes.append(df)

    # Database - Read from SQL tables
    db_dataframes = []
    for country, (conn_id, table) in DB_CONNECTIONS.items():
        if conn_id.startswith("mysql"):
            hook = MySqlHook(mysql_conn_id=conn_id)
            df = hook.get_pandas_df(f"SELECT * FROM {table}")
            df["Country"]=f"{table.split('_')[0]}"
        elif conn_id.startswith("postgres"):
            hook = PostgresHook(postgres_conn_id=conn_id)
            df = hook.get_pandas_df(f'SELECT * FROM "{table}"')
            df["Country"]="Norway"
        elif conn_id.startswith("mssql"):
            hook = MsSqlHook(mssql_conn_id=conn_id)
            df = hook.get_pandas_df(f"SELECT * FROM {table}")
            df["Country"]="India"
        else:
            raise ValueError("Unsupported DB type")

        db_dataframes.append(df)

    # Combine GCS data and database data
    all_data = pd.concat(dataframes + db_dataframes, ignore_index=True)
    
    return all_data

def clean_and_transform_data(df, **kwargs):
    """
    This function performs the necessary data transformations
    such as calculating amounts, converting currencies, and cleaning.
    """
    if df.empty:
        raise ValueError("Dataframe is empty, no data to process")

    # 1. Clean the data (remove rows with null values)
    df = df.dropna()

    # 2. Calculate 'Amount' and 'INR_Amount'
    df["Amount"] = df["Qty"] * df["Sale"]
    df["INR_Amount"] = df["Amount"] * df["Country"].map(CURRENCY_RATES).fillna(1)


    # 4. You can add any additional cleaning/transformation steps here

    return df

def load_to_bigquery(df, **kwargs):
    """
    This function will load the transformed data into BigQuery.
    """
    if df.empty:
        raise ValueError("No data to load to BigQuery")

    # BigQuery client setup
    client = bigquery.Client()
    dataset_id = "p2project-460510.testdb"  # Replace with your project and dataset name
    table_id = f"{dataset_id}.cleaned_table"  # Example table name

    job_config = bigquery.LoadJobConfig(
        schema=[
            bigquery.SchemaField("SaleId", "STRING"),
            bigquery.SchemaField("Country", "STRING"),
            bigquery.SchemaField("Category", "STRING"),
            bigquery.SchemaField("Product", "STRING"),
            bigquery.SchemaField("Qty", "INTEGER"),
            bigquery.SchemaField("Sale", "FLOAT"),
            bigquery.SchemaField("Amount", "FLOAT"),
            bigquery.SchemaField("INR_Amount", "FLOAT"),
        ],
        write_disposition="WRITE_TRUNCATE",  # Append to the table (or use WRITE_TRUNCATE)
    )

    # Load the dataframe to BigQuery
    client.load_table_from_dataframe(df, table_id, job_config=job_config)

def create_etl_task(**kwargs):
    # Step 1: Read and combine data from both GCS and DB
    df_combined = read_and_combine_data(**kwargs)

    # Step 2: Clean and transform data
    df_cleaned = clean_and_transform_data(df_combined, **kwargs)

    # Step 3: Load the transformed data to BigQuery
    load_to_bigquery(df_cleaned, **kwargs)

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

dag = DAG(
    dag_id='etl_clean_transform_and_load_to_bigquery',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False,
    description='Read, clean, transform, and load data from GCS and databases to BigQuery'
)

etl_task = PythonOperator(
    task_id="etl_process_to_bigquery",
    python_callable=create_etl_task,
    provide_context=True,
    dag=dag
)

etl_task
