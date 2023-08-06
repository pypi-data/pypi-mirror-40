from datetime import datetime
from typing import List, Any

import boto3


def s3_bucket(bucket: str) -> Any:
    s3_resource = boto3.resource('s3')
    return s3_resource.Bucket(name=bucket)


def get_object(bucket_name: str, key: str) -> Any:
    bucket = s3_bucket(bucket_name)
    obj = bucket.Object(key=key)
    return obj.get().get('Body').read()


def put_object(bucket_name: str, key: str, content: str):
    bucket = s3_bucket(bucket_name)
    obj = bucket.Object(key=key)
    obj.put(Body=content, ContentType='application/json')


def list_objects(bucket_name: str, path: str = None) -> List[Any]:
    bucket = s3_bucket(bucket_name)
    return [obj.key for obj in bucket.objects.filter(
        Prefix=path if path else ''
    )]


def build_key(dt: datetime, subject: str) -> str:
    path = dt.strftime('%Y/%m/%d/%H')
    time = dt.strftime('%M%S%f')
    return f'{path}/{subject}_{time}.json'
