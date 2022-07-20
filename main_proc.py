from selenium import webdriver
from tempfile import mkdtemp
from selenium.webdriver.common.by import By
import boto3
import os
import logging
from botocore.exceptions import ClientError
from datetime import datetime

# sls invoke --function screenshot_proc --raw --data https://www.example.com/

format = ".jpg"
s3_bucket = "stg-uploaded-screenshots-lambda"
s3_client = boto3.client('s3')

def handler(event=None, context=None):
    options = webdriver.ChromeOptions()
    options.binary_location = '/opt/chrome/chrome'
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280x1696")
    options.add_argument("--single-process")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-dev-tools")
    options.add_argument("--no-zygote")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.add_argument(f"--data-path={mkdtemp()}")
    options.add_argument(f"--disk-cache-dir={mkdtemp()}")
    options.add_argument("--remote-debugging-port=9222")
    chrome = webdriver.Chrome("/opt/chromedriver",
                              options=options)
    chrome.get(event)

    try:
        today = datetime.now()
        file_name = "Picture" + str(today)
        path = "/tmp"
        output_path = path + "/output/"
        file_path_full = output_path + file_name

        if os.path.exists(output_path):
            print("Dir exists")
        else:
            os.makedirs(output_path)

        chrome.find_element(By.TAG_NAME, 'body').screenshot(file_path_full)
        upload = s3_client.upload_file(file_path_full, s3_bucket, file_name)
    except Exception as e:
        return str(e)

    return chrome.find_element(by=By.XPATH, value="//html").text


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True