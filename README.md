# serverless-csv-exporter
The application reads the content of csv, and writes them into a database.
This lambda function is triggered whenever a CSV file is uploaded to the S3 bucked called `bucket-for-csv-files`

## Technical Details
- Python version 3.8.6
- Mysql version 5.7


## Manuel Steps
- First, you should install the imported requesties.

- To work in AWS,
    - Zip the application `main.py` with the installed requirements, and name the zip as `1.zip`
    - Upload the zip to the S3 bucket called `resources-ayy-1/csv_content_exporter/`
    - To trigger the application, upload a csv file into the S3 bucked called `bucket-for-csv-files`

- You can otomatize to change zip file name by putting the code below in a Jenkins file (or any CI/CD tool)
    - Therefore, you can update the s3_key name with the newest zip name
    - First, upload the zip to s3
        * `aws s3 cp ${BUILD_ID}.zip s3://bucket-for-csv-files/csv_content_exporter/${BUILD_ID}.zip --region eu-west-1`
    - Then update the lambda function s3_key name
        * `aws lambda update-function-code --function-name csv-content-exporter --s3-bucket resources-ayy-1 --s3-key csv_content_exporter/ /${BUILD_ID}.jar --region eu-west-1`

