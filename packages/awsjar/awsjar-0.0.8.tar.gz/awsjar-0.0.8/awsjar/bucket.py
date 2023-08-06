import json

import boto3
from botocore import exceptions

from awsjar.utils import _data_dumper
from awsjar.exceptions import ClientError


class Bucket:
    def __init__(self, *, bucket, key, region="", encoder=None, decoder=None):
        if region:
            self._s3 = boto3.resource("s3", region_name=region)
            self._cl = boto3.client("s3", region_name=region)
        else:
            self._s3 = boto3.resource("s3")
            self._cl = boto3.client("s3")

        self.key = key
        self.bucket_name = bucket

        self._does_bucket_exist(bucket)
        self.bucket = self._s3.Bucket(bucket)

        if self._is_versioning_enabled():
            self.get = self._get_latest_version_of_obj
        else:
            self.get = self._get

        if not encoder:
            encoder = str

        def _dumps(data):
            return json.dumps(data, default=encoder)

        def _loads(data):
            return json.loads(data, object_hook=decoder)

        self._dumps = _dumps
        self._loads = _loads

    def _is_versioning_enabled(self):
        ver = self.bucket.Versioning()
        status = ver.status
        if status and status == "Enabled":
            return True
        return False

    def enable_versioning(self):
        ver = self.bucket.Versioning()
        ver.enable()
        self.get = self._get_latest_version_of_obj

    def disable_versioning(self):
        ver = self.bucket.Versioning()
        ver.suspend()
        self.get = self._get

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

    def _get(self, key=""):
        """ Get and decode stored state from S3. If the object does not exist, return an empty dict
        :param key: Key can be specified if you want to fetch something over than self.key
        :return: list or dict
        """
        if key:
            k = key
        else:
            k = self.key

        try:
            obj = self._s3.Object(self.bucket_name, k)
            state = obj.get()
            state = state["Body"].read().decode()
        except exceptions.ClientError as e:
            err = e.response["Error"]
            print("err:", err)
            if err["Code"] == "403" and err["Message"] == "Forbidden":
                msg = f"Received forbidden when trying to access S3 object: s3://{self.bucket_name}/{k}"
                raise ClientError(msg)
            elif (
                err["Code"] == "NoSuchKey"
                and err["Message"] == "The specified key does not exist."
            ):
                return {}
            else:
                raise Exception(e)

        state = self._loads(state)
        return state

    def _get_latest_version_of_obj(self, key=""):
        """ Get and decode stored state from S3. If the object does not exist, return an empty dict.
        :param key: Key can be specified if you want to fetch something over than self.key
        :return: list or dict
        """
        if key:
            k = key
        else:
            k = self.key
        obj = self._get_latest_object_version(k)
        if not obj:
            msg = f"Latest version id was not found for s3://{self.bucket_name}/{key} while trying to get the object."
            raise ClientError(msg)
        state = obj.get()["Body"].read().decode()
        state = self._loads(state)
        return state

    def _does_bucket_exist(self, bucket):
        """ Determine if bucket exists and if we have necessary access to it """
        try:
            self._cl.head_bucket(Bucket=bucket)
        except exceptions.ClientError as e:
            err = e.response["Error"]
            if err["Code"] == "403" and err["Message"] == "Forbidden":
                msg = (
                    f"Received forbidden when trying to access S3 bucket: s3://{bucket}"
                )
                raise ClientError(msg)
            elif err["Code"] == "404" and err["Message"] == "Not Found":
                msg = (
                    f"Received not found when trying to access S3 bucket: s3://{bucket}"
                )
                raise ClientError(msg)
            else:
                raise Exception(e)

    def _get_latest_object_version(self, key=""):
        """ Get latest object version.
        :param key: Key can be specified if you want to fetch something over than self.key
        :return: Latest version id of object
        """
        if key:
            k = key
        else:
            k = self.key

        versions = self.bucket.object_versions.filter(Prefix=k)
        for version in versions:
            if version.is_latest:
                return version
        return None


if __name__ == "__main__":
    b = Bucket(bucket="awsjarbucket", key="asdf")
    k = b._get_latest_version_of_obj(key="asdfaasdassda")
    print(k)
    print(b.get(key="asdfaasdassda"))
