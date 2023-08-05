from future.standard_library import install_aliases  # noqa
install_aliases()  # noqa
from urllib.parse import urlparse
import json
import io
import os

import boto3
from botocore.exceptions import ClientError

from ..utils import mkdir_p


s3 = boto3.client('s3')


RF_ACCESS_POLICY = {
    'Sid': 'RasterFoundryReadWriteAccess',
    'Effect': 'Allow',
    'Principal': {
        'AWS': 'arn:aws:iam::615874746523:root'
    },
    'Action': [
        's3:GetObject',
        's3:ListBucket',
        's3:PutObject'
    ],
    'Resource': [
        'arn:aws:s3:::{}',
        'arn:aws:s3:::{}/*'
    ]
}


def authorize_bucket(bucket_name):
    """Authorize Raster Foundry to read and write from an S3 bucket

    Args:
        bucket_name (str): the name of the bucket to authorize

    Returns:
        int: the status code from the attempted policy change
    """

    rf_access_policy = RF_ACCESS_POLICY.copy()
    rf_access_policy['Resource'] = [
        x.format(bucket_name) for x in rf_access_policy['Resource']
    ]

    try:
        resp = s3.get_bucket_policy(Bucket=bucket_name)
        existing_policy = json.loads(resp['Policy'])
    except ClientError:
        existing_policy = {
            'Version': '2012-10-17',
            'Statement': []
        }

    existing_policy['Statement'].append(rf_access_policy)
    new_policy_str = json.dumps(existing_policy)
    return s3.put_bucket_policy(
        Bucket=bucket_name, Policy=new_policy_str
    )['ResponseMetadata']['HTTPStatusCode']


def unauthorize_bucket(bucket_name):
    """Remove Raster Foundry authorization from a bucket

    Args:
        bucket_name (str): the name of the bucket to unauthorize

    Returns:
        int: the status code from the attempted policy change
    """
    rf_access_policy = RF_ACCESS_POLICY.copy()
    rf_access_policy['Resource'] = [
        x.format(bucket_name) for x in rf_access_policy['Resource']
    ]

    try:
        resp = s3.get_bucket_policy(Bucket=bucket_name)
        existing_policy = json.loads(resp['Policy'])
    except ClientError:
        existing_policy = {
            'Version': '2012-10-17',
            'Statement': []
        }

    if rf_access_policy in existing_policy['Statement']:
        new_statement = [
            x for x in existing_policy['Statement'] if x != rf_access_policy
        ]
        existing_policy['Statement'] = new_statement
        if new_statement:
            new_policy_str = json.dumps(existing_policy)
            resp = s3.put_bucket_policy(
                Bucket=bucket_name, Policy=new_policy_str
            )['ResponseMetadata']['HTTPStatusCode']
        else:
            resp = s3.delete_bucket_policy(Bucket=bucket_name)
    else:
        # No work to do, so just create a mock response
        resp = {'ResponseMetadata': {'HTTPStatusCode': 204}}

    return resp['ResponseMetadata']['HTTPStatusCode']


def file_to_str(file_uri):
    parsed_uri = urlparse(file_uri)
    if parsed_uri.scheme == 's3':
        with io.BytesIO() as file_buffer:
            s3.download_fileobj(
                parsed_uri.netloc, parsed_uri.path[1:], file_buffer)
            return file_buffer.getvalue().decode('utf-8')
    else:
        with open(file_uri, 'r') as file_buffer:
            return file_buffer.read()


def str_to_file(content_str, file_uri):
    parsed_uri = urlparse(file_uri)
    if parsed_uri.scheme == 's3':
        bucket = parsed_uri.netloc
        key = parsed_uri.path[1:]
        with io.BytesIO(bytes(content_str, encoding='utf-8')) as str_buffer:
            s3.upload_fileobj(str_buffer, bucket, key)
    else:
        mkdir_p(os.path.dirname(file_uri))
        with open(file_uri, 'w') as content_file:
            content_file.write(content_str)
