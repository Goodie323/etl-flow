Overview
========

 ETL Project with Apache Airflow (Astronomer)
Welcome to my ETL project powered by Apache Airflow using Astronomer CLI. This setup was initialized with astro dev init and is designed to streamline and orchestrate data pipelines locally before deploying to production environments

Project Contents
================
Project Structure
This project includes the following directories and files:

dags/
Contains your Airflow DAGs (Directed Acyclic Graphs).

example_astronauts.py: A sample DAG that demonstrates a simple ETL process. It fetches data from the Open Notify API to list astronauts currently in space using the TaskFlow API and dynamic task mapping.
💡 Great for getting started!

include/
For any additional resources (e.g. SQL files, templates). Empty by default.

plugins/
Add custom or community Airflow plugins here. Empty by default.

Dockerfile
Defines the Astro Runtime Docker image. Customize it for your project-specific execution or dependency overrides.

requirements.txt
List all Python dependencies required for your DAGs or tasks.

packages.txt
Add OS-level packages here if needed (e.g. libsasl2-dev, unixODBC, etc.).

airflow_settings.yaml
Configure Airflow Connections, Variables, and Pools locally instead of using the UI. Ideal for reproducibility.

Deploy Your Project Locally
===========================

Start Airflow on your local machine by running 'astro dev start'.

This command will spin up five Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Scheduler: The Airflow component responsible for monitoring and triggering tasks
- DAG Processor: The Airflow component responsible for parsing DAGs
- API Server: The Airflow component responsible for serving the Airflow UI and API
- Triggerer: The Airflow component responsible for triggering deferred tasks

When all five containers are ready the command will open the browser to the Airflow UI at http://localhost:8080/. You should also be able to access your Postgres Database at 'localhost:5432/postgres' with username 'postgres' and password 'postgres'.

Note: If you already have either of the above ports allocated, you can either [stop your existing Docker containers or change the port](https://www.astronomer.io/docs/astro/cli/troubleshoot-locally#ports-are-not-available-for-my-local-airflow-webserver).

 Contributing
=================================

 Contributing
Feel free to clone, fork, or contribute to this project. This setup serves as a boilerplate for developing scalable and robust ETL pipelines with Apache Airflow.e/


