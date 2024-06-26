﻿# MLOps_Assignment2_i202308

This README provides a detailed guide for installing Apache Airflow on a Linux system, starting its services, and creating a new user. Follow these instructions to ensure a smooth setup of Airflow for managing and automating your data workflows.

## Prerequisites

Before you install Apache Airflow, ensure your system meets the following requirements:
- Python version 3.6, 3.7, 3.8, or 3.9
- pip (Python package installer)

You can check your Python and pip versions by running:

```bash
python --version
pip --version
```

If Python is not installed, you can install it using your system's package manager. For Debian-based systems like Ubuntu or Kali Linux:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

## Environment Setup

It's recommended to use a virtual environment to avoid conflicts with other Python projects.

Create and activate a virtual environment:

```bash
python3 -m venv airflow_venv
source airflow_venv/bin/activate
```

## Installing Apache Airflow

1. **Set AIRFLOW_HOME (Optional)**:

   You can define where Airflow stores its configuration and instance files:

   ```bash
   export AIRFLOW_HOME=~/airflow
   ```

2. **Install Apache Airflow**:

   Use pip to install Airflow, specifying the version and constraints to ensure compatibility:

   ```bash
   AIRFLOW_VERSION=2.4.2
   PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
   CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
   pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
   ```

## Initialize the Airflow Database

Airflow uses a database to manage state and configuration. By default, it uses SQLite.

Initialize the database with:

```bash
airflow db init
```

## Start Airflow Services

1. **Web Server**:

   Start the web server on the default port (8080):

   ```bash
   airflow webserver --port 8080
   ```

2. **Scheduler**:

   Open another terminal, activate your virtual environment, and start the scheduler:

   ```bash
   airflow scheduler
   ```

## User Management

Create a new user for accessing the Airflow web interface:

```bash
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

You will be prompted to enter a password for the new user.

## Accessing the Airflow Web Interface

With the web server running, you can access the Airflow UI by navigating to:

```
http://localhost:8080
```

Log in with the credentials of the user you just created.

## Verifying the Installation

Ensure that Airflow is correctly set up by listing all users:

```bash
airflow users list
```

This command will show all the users configured in your Airflow instance.

## Conclusion

Congratulations! You now have Apache Airflow installed and configured on your Linux system. You can start defining DAGs to automate and manage your workflows.

For more detailed information and advanced configurations, refer to the [official Apache Airflow documentation](https://airflow.apache.org/docs/).
```

This README file is designed to be thorough and user-friendly, guiding new users through each step required to get Apache Airflow up and running on their system. It covers initial setup, environment configuration, installation, service management, and user creation, providing a solid foundation for starting with Airflow.
