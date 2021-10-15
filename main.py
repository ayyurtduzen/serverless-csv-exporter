import boto3
import os
import csv
import mysql.connector
import sys

# Environment variables for the app to connect
# Values are coming from infra
database  = os.getenv('MYSQL_DB_NAME')
port   = os.getenv('MYSQL_DB_PORT')
username  = os.getenv('MYSQL_DB_USER')
password  = os.getenv('MYSQL_DB_PASSWORD_SECRET_NAME')
hostname  = 'master-database.citqrnpqipqm.eu-west-1.rds.amazonaws.com'
s3_bucket = os.getenv('S3_BUCKET_NAME')
s3_key = os.getenv('S3_KEY_NAME')

# Creates the table first
# For other times, it skips this method
def create_student_table(connection):
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students_list (
    StudentID INT PRIMARY KEY,
    StudentName VARCHAR(255),
    StudentLastname VARCHAR(255),
    Attendance BOOLEAN
    );
    """
)

def lambda_handler(event, context):
    status = 'DONE'
    # Try to connect the database, otherwise send an error
    try:
        connection = mysql.connector.connect(
            hostname, user=username, password=password, host=hostname, port=port, db=database
            )
    except mysql.connector.Error as e:
        print(f"Getting error to connect student database: {e}")
        sys.exit(1)

    # Create the table first
    create_student_table(connection)

    # Read data from csv file in the S3 bucket
    s3_client        = boto3.client('s3')
    bucket_name      = s3_bucket
    key_name        = s3_key
    csv_file         = s3_client.get_object(Bucket=bucket_name, Key=key_name)
    csv_file_content = csv_file['Body'].read().decode('utf-8').splitlines()
    rows             = csv.reader(csv_file_content)

    attendance_list = []
    for row in rows:
        student = {}
        student["StudentID"]       = row[0]
        student["StudentName"]     = row[1]
        student["StudentLastname"] = row[2]
        student["Attendance"]      = row[3]
        attendance_list.append(student)

    # Write the data into the Mysql Database Table
    for student in attendance_list:
        cur = connection.cursor()
        sql_query = "INSERT INTO Users (StudentID, StudentName , StudentLastname , Attendance) VALUES (%s, %s , %s , %s)"
        values = (student["StudentID"],student["StudentName"],student["StudentLastname"],student["Attendance"])
        cur.execute(sql_query, values)
        connection.commit()

    connection.close()

    return status
