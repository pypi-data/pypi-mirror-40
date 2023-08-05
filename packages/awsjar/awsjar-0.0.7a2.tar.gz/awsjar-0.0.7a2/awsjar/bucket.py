import json

import boto3
from botocore import exceptions
from .utils import _data_dumper
from .exceptions import ClientError


class Bucket:
    def __init__(self, *, bucket, key, region="", encoder=None, decoder=None):
        if region:
            self._s3 = boto3.resource("s3", region_name=region)
            self._cl = boto3.client("s3", region_name=region)
        else:
            self._s3 = boto3.resource("s3")
            self._cl = boto3.client("s3")

        self.key = f"{key}.json"

        self._does_bucket_exists(bucket)
        self.bucket = self._s3.Bucket(bucket)

        if not encoder:
            encoder = str

        def _dumps(data):
            return json.dumps(data, default=encoder)

        def _loads(data):
            return json.loads(data, object_hook=decoder)

        self._dumps = _dumps
        self._loads = _loads

    def put(self, data):
        """
        Enocde data into json then put it on S3
        :param data: Either a list or dict
        :return: Boto3 S3 Bucket Resource Object
        https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Bucket.put_object
        """
        data = _data_dumper(data, self._dumps)

        resp = self.bucket.put_object(Body=data, Key=self.key)
        return resp

    def get(self):
        """ Get and decode stored state from S3. If the object does not exist, return an empty dict
        :return: list or dict
        """
        try:
            self.bucket.download_file(self.key, "/tmp/bucket.tmp")
        except exceptions.ClientError as e:
            err = e.response["Error"]
            if err["Code"] == "403" and err["Message"] == "Forbidden":
                raise ClientError('Received forbidden when trying to access S3 object.')
            elif err["Code"] == "404" and err["Message"] == "Not Found":
                return {}
            else:
                raise Exception(e)

        with open("/tmp/bucket.tmp", "r") as data:
            x = data.read()
            state = self._loads(x)

        return state

    def _does_bucket_exists(self, bucket):
        try:
            self._cl.head_bucket(
                Bucket=bucket
            )
        except exceptions.ClientError as e:
            err = e.response["Error"]
            if err["Code"] == "403" and err["Message"] == "Forbidden":
                raise ClientError('Received forbidden when trying to access S3 bucket.')
            if err["Code"] == "404" and err["Message"] == "Not Found":
                raise ClientError('Received not found when trying to access S3 bucket.')
            else:
                raise Exception(e)
