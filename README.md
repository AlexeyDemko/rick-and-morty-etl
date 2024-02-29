## Language Version
Python Version: 3.11

## Resource Requirements:
CPU: Minimum 2 cores, recommended 4 cores
RAM: Minimum 4 GB, recommended 8 GB

## Required Packages
Install the following dependencies from the requirements.txt file:
- psycopg2-binary==2.9.9
- requests==2.31.0

## Technologies Used
- ETL Tool: Airflow
- Database: Postgres
- Docker

## Installation
1. Download and install Docker Desktop.
2. Clone repository.
```bash
  git clone https://github.com/AlexeyDemko/rick-and-morty-etl.git
```
3. Execute
4. ```bash
   docker-compose up -d
   ```
5. Access application services via the web browser:
    
    * Airflow UI - `http://localhost:8080/`
6. Enter username and password (default values - `airflow`).
7. To begin the ETL process, click on the left side to start the DAG. Additionally, you can manually trigger the DAG if needed.
8. Data will be stored in the configured database. You can access it for example via docker container:
```bash
docker exec -it rick-and-morty-etl-db-1 psql -U rick -d rick
```
After that make SQL-query to the `chars_appearance` table.
