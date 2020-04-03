from plots import country_incremental_comparison, country_total_comparison, save_plot
import boto3
import io
import json

# todo make AWS resource name defined in a global config file
# so that it can be accessed in yaml and python

def my_handler(event, context):
    country_names = [
        "United States",
        "Italy",
        "South Korea",
        "China",
        "Canada"]

    bucket_name = "covid-19-plots"
    country_incremental_comparison(country_names)
    img_data = io.BytesIO()
    save_plot(img_data)
    img_data.seek(0)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(Body=img_data, ContentType='image/png', Key="country_incrementals.png")

    country_total_comparison(country_names)
    img_data = io.BytesIO()
    save_plot(img_data)
    img_data.seek(0)
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.put_object(Body=img_data, ContentType='image/png', Key="country_totals.png")

    client = boto3.client('sns')
    message = {"covid19-update": "success"}
    response = client.publish(
        TargetArn="arn:aws:sns:us-west-2:328555735540:Covid19Topic",
        Message=json.dumps(message)
    )

    return {
        'message': "ok"
    }
