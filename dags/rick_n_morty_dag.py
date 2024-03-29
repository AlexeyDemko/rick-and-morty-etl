import json
import sys
import logging
from collections import defaultdict
from datetime import datetime

import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

sys.path.append("/opt/airflow/src")

from db_utils import execute_query

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime.now(),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1
}

URLS = {"char": "https://rickandmortyapi.com/api/character",
        "episode": "https://rickandmortyapi.com/api/episode"}


def extract_task():
    chars_data = []
    episodes_data = {}

    for key, url in URLS.items():
        while url:
            try:
                response = requests.get(url)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                raise Exception(f"Failed to fetch data from {url}: {e}")

            data = response.json()

            if key == "char":
                chars_data.extend(data["results"])
                url = data["info"]["next"]
            elif key == "episode":
                for episode in data["results"]:
                    episodes_data[episode["url"]] = episode["air_date"]
                url = data["info"]["next"]

    return json.dumps(chars_data), json.dumps(episodes_data)


def transform_task(chars_data_json, episodes_data_json):
    chars_count_by_month = defaultdict(int)
    chars_data = json.loads(chars_data_json)
    episodes_data = json.loads(episodes_data_json)
    for character in chars_data:
        try:
            if character["origin"]["name"] == "Earth (C-137)":
                try:
                    for episode in character["episode"]:
                        episode_date = datetime.strptime(episodes_data[episode], "%B %d, %Y")
                        chars_count_by_month[episode_date.strftime("%Y-%m")] += 1
                except ValueError as ve:
                    logging.error(f"Error parsing date for episodes. Error: {ve}")
        except Exception as ex:
            logging.error(f"Error parsing character data. Error: {ex}")

    return json.dumps(chars_count_by_month)


def load_task(chars_count_by_month_json):
    chars_count_by_month = json.loads(chars_count_by_month_json)
    if chars_count_by_month:
        execute_query("""TRUNCATE TABLE chars_appearance""")
        for episode_date_str, chars_count in chars_count_by_month.items():
            try:
                episode_date = datetime.strptime(episode_date_str, "%Y-%m")
                execute_query("""
                    INSERT INTO chars_appearance (episode_date, chars_count) 
                    VALUES (%(episode_date)s, %(chars_count)s)
                """, {"episode_date": episode_date, "chars_count": chars_count})
            except Exception as e:
                logging.error(f"Error processing entry: {episode_date_str}: {chars_count}. Error: {e}")


with DAG(
        'rick_and_morty_pipeline',
        default_args=default_args,
        description='A simple DAG to load Rick and Morty data into Postgres',
        schedule_interval='@once',
) as dag:
    extract_task = PythonOperator(
        task_id='extract_task',
        python_callable=extract_task,
    )

    transform_task = PythonOperator(
        task_id='transform_task',
        python_callable=transform_task,
        op_args=['{{ task_instance.xcom_pull(task_ids="extract_task")[0] }}',
                 '{{ task_instance.xcom_pull(task_ids="extract_task")[1] }}'],

    )

    load_task = PythonOperator(
        task_id='load_task',
        python_callable=load_task,
        op_args=['{{ task_instance.xcom_pull(task_ids="transform_task") }}'],
    )

    extract_task >> transform_task >> load_task
