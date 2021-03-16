import os
import subprocess
import tempfile
import urllib

import boto3
from airflow.models import Variable
from io import BytesIO
from zipfile import ZipFile


def upload_to_s3():
    """
        Scrape geo-data from geoname to s3.
    """
    url = urllib.request.urlopen("http://download.geonames.org/export/zip/IN.zip")

    client = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=Variable.get('aws_default_region')
    )

    with ZipFile(BytesIO(url.read())) as my_zip_file:
        for contained_file in my_zip_file.namelist():
            if contained_file == "IN.txt":
                with my_zip_file.open(contained_file, 'r') as data:
                    client.upload_fileobj(data, 's3-bucket', 'path/IN.txt')


def download_upload_s3():
    client = boto3.client(
        's3',
        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
        region_name=Variable.get('aws_default_region'),
    )

    with tempfile.TemporaryDirectory() as tmpdirname:
        output_filename = os.path.join(tmpdirname, 'model')
        client.download_file("bucket", "key", output_filename)

        tc = subprocess.call([
            "tar",
            "xzf",
            output_filename,
            f"--directory={tmpdirname}",
        ])
        assert tc == 0, 'tar error'
        print('extracted', str(os.listdir(tmpdirname)))

        df_filename = os.path.join(tmpdirname, "file-name")
        client.upload_file(df_filename, "bucket", "key")
