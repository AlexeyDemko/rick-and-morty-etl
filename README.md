## Technologies Used
- ETL Tool: Airflow
- Database: Postgres
- Docker

## Usage
1. Download and install Docker Desktop.
2. Clone repository.
```bash
  git clone https://github.com/AlexeyDemko/rick-and-morty-etl.git
```
3. Execute docker-compose up -d
4. Access application services via the web browser:
    
    * Airflow UI - `http://localhost:8080/`
5. Enter username and password (default values - `airflow`).
5. Manually trigger the dag to start ETL process.
6. Data will be stored in the configured database.