import io
import json
import os

import boto3

from plots import (country_incremental_comparison, country_total_comparison,
                   save_plot)

# todo make AWS resource name defined in a global config file
# so that it can be accessed in yaml and python


def generate_graph_save_to_s3(bucket, key):
    img_data = io.BytesIO()
    save_plot(img_data)
    img_data.seek(0)
    bucket.put_object(Body=img_data, ContentType='image/png', Key=key)


def get_object_url(s3_bucket_name, key_name):
    bucket_location = boto3.client(
        's3').get_bucket_location(Bucket=s3_bucket_name)
    object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
        bucket_location['LocationConstraint'],
        s3_bucket_name,
        key_name)
    return object_url


def my_handler(event, context):
    country_names = os.environ["CountriesToPlot"].split(",")

    print("Generating graphs")
    bucket_name = os.environ["CovidBucketName"]
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    inrementals_key = os.environ["S3IncrementalObjectKey"]
    country_incremental_comparison(country_names)
    generate_graph_save_to_s3(bucket, inrementals_key)

    totals_key = os.environ["S3TotalObjectKey"]
    country_total_comparison(country_names)
    generate_graph_save_to_s3(bucket, totals_key)

    print("Sending notifications")
    client = boto3.client('sns')
    message = {"incrementals": get_object_url(bucket_name, inrementals_key),
               "totals": get_object_url(bucket_name, totals_key)}

    response = client.publish(
        TargetArn=os.environ["SNSTopic"],
        Message=json.dumps(message)
    )

    return {
        'message': "ok"
    }
