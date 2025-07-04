from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from datetime import datetime, timedelta
from airflow.utils import timezone
import requests
import logging

# Constants
LATITUDE = "51.5074"
LONGITUDE = "-0.1278"
POSTGRES_CONN_ID = "postgres_default"

default_args = {
    "owner": "airflow",
    "start_date": timezone.utcnow() - timedelta(days=1),  # Fixed start_date
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# DAG Definition
with DAG(
    dag_id="weather_etl_pipeline_no_http_hook",
    default_args=default_args,
    schedule="@daily",  # Replaced schedule_interval
    catchup=False,
    tags=["example"],
) as dag:

    @task
    def extract_weather_data():
        """Extract weather data from Open-Meteo API."""
        url = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()  # Raises HTTPError for bad responses
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Failed to fetch weather data: {e}")
            raise

    @task
    def transform_weather_data(weather_data: dict) -> dict:
        """Transform raw weather data into a structured format."""
        current_weather = weather_data.get("current_weather", {})
        return {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "temperature": current_weather.get("temperature"),
            "windspeed": current_weather.get("windspeed"),
            "winddirection": current_weather.get("winddirection"),
            "weathercode": current_weather.get("weathercode"),
        }

    @task
    def load_weather_data(transformed_data: dict):
        """Load transformed data into PostgreSQL."""
        try:
            pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
            conn = pg_hook.get_conn()
            cursor = conn.cursor()

            # Create table if not exists
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weather_data (
                    latitude FLOAT,
                    longitude FLOAT,
                    temperature FLOAT,
                    windspeed FLOAT,
                    winddirection FLOAT,
                    weathercode INT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            # Insert data
            cursor.execute("""
                INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                transformed_data["latitude"],
                transformed_data["longitude"],
                transformed_data["temperature"],
                transformed_data["windspeed"],
                transformed_data["winddirection"],
                transformed_data["weathercode"],
            ))

            conn.commit()
        except Exception as e:
            logging.error(f"Failed to load data into PostgreSQL: {e}")
            raise
        finally:
            cursor.close()
            conn.close()

    # Define the workflow
    weather_data = extract_weather_data()
    transformed_data = transform_weather_data(weather_data)
    load_weather_data(transformed_data)