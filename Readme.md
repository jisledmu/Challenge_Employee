# Employee Data API

This project is an API built with **FastAPI** for managing employees, departments, and jobs, using an **SQLite** database. It provides endpoints to upload data from **CSV** files, create backups in **AVRO** format, restore tables from backups, and query statistics about employees.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Usage](#usage)
  - [Upload and Process a CSV File](#upload-and-process-a-csv-file)
  - [Restore a Table from Backup](#restore-a-table-from-backup)
  - [Query Employees by Job and Department in 2021](#query-employees-by-job-and-department-in-2021)
  - [Query Departments with Hiring Above Average](#query-departments-with-hiring-above-average)
- [CSV File Structure](#csv-file-structure)
- [Errors and Log](#errors-and-log)
- [Using Swagger with the API]

## Requirements

- Python 3.8+
- FastAPI
- Pydantic
- SQLite3
- pandas
- fastavro
- uvicorn (for running the server)

## Installation

Follow these steps to install and run the project:

```bash
# Clone the repository
git clone https://github.com/username/project.git

# Navigate to the project directory
cd project

# Create a virtual environment (optional but recommended)
python3 -m venv env
source env/bin/activate  # On Linux/macOS
env\Scripts\activate     # On Windows
```

# Install dependencies
pip install -r requirements.txt

## Installation

1. Clone the repository or download the files.

2. Install the dependencies using pip:

```bash
  pip install fastapi pandas sqlite3 fastavro uvicorn
```

3. Create the SQLite3 database at the specified path in the code, or update the `DATABASE_PATH` variable to use an existing database.

## Project Structure

- **models**: Defines the Pydantic models for `HiredEmployee`, `Department`, and `Job`.
- **API endpoints**: Includes methods for uploading CSV files, creating AVRO backups, restoring from AVRO, and performing specific queries.
- **Additional Functions**: Data validation, table creation and verification, and error logging.

## Usage

To start the FastAPI server, use the following command:

```bash
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000.

Upload and Process a CSV File
Upload a CSV file to insert or update data in the corresponding table. The table will be automatically created if it doesn't exist.

Endpoint: /upload-csv/
Method: POST
Parameter: file (CSV file to upload)
Example request using curl:

bash
```
curl -X POST "http://127.0.0.1:8000/upload-csv/" -F "file=@/path/to/file.csv"
```

## Restore a Table from Backup

Restores the data of a table from an AVRO backup file.

- **Endpoint**: `/restore-table/`
- **Method**: `POST`
- **Parameter**: `table_name` (name of the table to restore)

Example request using `curl`:

```bash
curl -X POST "http://127.0.0.1:8000/restore-table/" -H "Content-Type: application/json" -d '{"table_name": "employees"}'
```

## Query Employees by Job and Department in 2021

Queries the employees hired by department and job during 2021, organized by quarter.

- **Endpoint**: `/employees-by-job-and-department/`
- **Method**: `GET`

Example request:

```bash
curl -X GET "http://127.0.0.1:8000/employees-by-job-and-department/"
```

## Query Departments with Hiring Above Average

Queries the departments with hiring rates above the average in 2021.

- **Endpoint**: `/departments-above-average/`
- **Method**: `GET`

Example request:

```bash
curl -X GET "http://127.0.0.1:8000/departments-above-average/"
```

## CSV File Structure

The CSV files should follow these column structures:

- **hired_employees.csv**: `id`, `name`, `datetime`, `department_id`, `job_id`
- **departments.csv**: `id`, `department`
- **jobs.csv**: `id`, `job`

## Errors and Log

Errors, such as invalid rows in the CSV files, will be logged in the file `transaction_errors.log`.

## Using Swagger with the API

FastAPI automatically includes interactive documentation with Swagger, which you can access once the server is running. To use Swagger with this API, follow these steps:

### Steps to Use Swagger with the API

1. **Start the server**: Run the following command to start the FastAPI server:

    ```bash
    uvicorn main:app --reload
    ```

2. **Access the Swagger interface**: Once the server is running, open your browser and go to the following URL:

    ```Chrome
    http://127.0.0.1:8000/docs
    ```

   Here, you will find the Swagger-generated documentation, which will display all API endpoints along with details on HTTP methods, parameters, and possible responses.

3. **Explore and Test the Endpoints**: The Swagger interface allows you to test the endpoints interactively. Each endpoint has a "Try it out" button that, when clicked, lets you send requests and see responses in real-time.

### Example Interaction with Swagger

Each endpoint will be documented in Swagger. Below are some examples:

1. **Upload a CSV File**
   - **Endpoint**: `POST /upload-csv/`
   - **Description**: Uploads a CSV file to process data and store it in the database.
   - In Swagger, click "Try it out", upload a CSV file, and send the request.

2. **Restore a Table from AVRO**
   - **Endpoint**: `POST /restore-table/`
   - **Description**: Allows restoring a table from the database from an AVRO file.
   - In Swagger, click "Try it out", enter the name of the table you want to restore, and send the request.

3. **Query Employees by Job and Department in 2021**
   - **Endpoint**: `GET /employees-by-job-and-department/`
   - **Description**: Returns the number of employees hired by each department and job type during 2021.
   - In Swagger, click "Try it out" and send the request.

4. **Query Departments with Hiring Above Average**
   - **Endpoint**: `GET /departments-above-average/`
   - **Description**: Displays the departments with hiring rates above the average in 2021.
   - In Swagger, click "Try it out" and send the request.

