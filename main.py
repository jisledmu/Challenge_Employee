from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel, field_validator, ValidationError  # Agregar ValidationError
import pandas as pd
import sqlite3
import os
import logging

app = FastAPI()

# Configuración de logging para registrar los errores
logging.basicConfig(level=logging.INFO, filename="transaction_errors.log", 
                    format="%(asctime)s - %(message)s")

# Define models for each table
class HiredEmployee(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int

    @field_validator('name', 'datetime', 'department_id', 'job_id', mode='before')
    def check_not_empty(cls, value, info):
        if value is None or value == "":
            raise ValueError(f"{info.field.name} cannot be empty or None")
        return value

class Department(BaseModel):
    id: int
    department: str

    @field_validator('department', mode='before')
    def check_not_empty(cls, value, info):
        if value is None or value == "":
            raise ValueError(f"{info.field.name} cannot be empty or None")
        return value

class Job(BaseModel):
    id: int
    job: str

    @field_validator('job', mode='before')
    def check_not_empty(cls, value, info):
        if value is None or value == "":
            raise ValueError(f"{info.field.name} cannot be empty or None")
        return value

DATABASE_PATH = r"C:\Users\vanessa.ledezma\Desktop\Vane\Mi CV\Globant\Challenge\Db_Challenge\Challenge_Employees.db"

# Function to get the SQLite connection
def get_connection():
    conn = sqlite3.connect(DATABASE_PATH)
    return conn

# Function to create a specific table if it doesn't exist
def create_table(conn, table_name: str):
    cursor = conn.cursor()
    
    if table_name == "departments":
        create_table_query = '''CREATE TABLE IF NOT EXISTS departments (
                                    id INTEGER,
                                    department VARCHAR(50) NOT NULL
                                );'''
    elif table_name == "jobs":
        create_table_query = '''CREATE TABLE IF NOT EXISTS jobs (
                                    id INTEGER,
                                    job VARCHAR(50) NOT NULL
                                );'''
    elif table_name == "hired_employees":
        create_table_query = '''CREATE TABLE IF NOT EXISTS hired_employees (
                                    id INTEGER,
                                    name TEXT NOT NULL,
                                    datetime TEXT NOT NULL,
                                    department_id INTEGER,
                                    job_id INTEGER
                                );'''
    else:
        raise ValueError(f"Unknown table name: {table_name}")
    
    cursor.execute(create_table_query)
    conn.commit()

# Function to map table names to their corresponding Pydantic models and column names
def get_model_and_columns_for_table(table_name: str):
    if table_name == "departments":
        return Department, ["id", "department"]
    elif table_name == "jobs":
        return Job, ["id", "job"]
    elif table_name == "hired_employees":
        return HiredEmployee, ["id", "name", "datetime", "department_id", "job_id"]
    else:
        raise ValueError(f"Unknown table name: {table_name}")

# Endpoint to upload and process CSV files
@app.post("/upload-csv/")
async def upload_csv(file: UploadFile):
    try:
        # Save the uploaded file temporarily
        file_path = f"./{file.filename}"
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract the table name from the file name
        table_name = os.path.splitext(file.filename)[0]

        # Connect to the database and create table if not exists
        conn = get_connection()
        try:
            create_table(conn, table_name)  # Create the table
            insert_data_from_csv(conn, file_path, table_name)  # Insert the data
        finally:
            conn.close()

        # Remove the temporary file
        os.remove(file_path)

        return {"message": f"Data from {file.filename} has been inserted into {table_name} table."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Function to insert data from a CSV file into the corresponding table with validation
def insert_data_from_csv(conn, file_path: str, table_name: str):
    # Read the CSV file into a DataFrame without headers (header=None)
    data = pd.read_csv(file_path, header=None)

    # Get the corresponding Pydantic model and column names
    Model, columns = get_model_and_columns_for_table(table_name)

    # Assign the column names manually based on the table
    data.columns = columns

    # Validate and insert each row
    valid_rows = []
    invalid_rows = []
    for index, row in data.iterrows():
        try:
            # Validate the row data with the Pydantic model
            validated_data = Model(**row.to_dict())
            valid_rows.append(validated_data.dict())
        except ValidationError as e:  # Esta línea captura el error de validación
            # Log invalid rows
            logging.error(f"Invalid row {index} in table {table_name}: {e}")
            invalid_rows.append((index, row.to_dict()))

    # Check if there are any valid rows to insert
    if valid_rows:
        # Insert the valid rows into the database
        cursor = conn.cursor()
        for row in valid_rows:
            columns = ", ".join(row.keys())
            placeholders = ", ".join("?" for _ in row)
            values = tuple(row.values())
            cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        conn.commit()

    # If there are invalid rows, register the error in the log
    if invalid_rows:
        logging.error(f"Failed to insert {len(invalid_rows)} rows into table {table_name}. Invalid rows: {invalid_rows}")
