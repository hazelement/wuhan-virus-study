from plots import country_incremental_comparison, country_total_comparison, save_plot
import boto3
import io


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

    return {
        'message': "ok"
    }
