# -*- coding: utf-8 -*-

import os

from boto.s3.key import Key
from boto.s3.connection import S3Connection

from presstatic.storage import Storage, FileStorageIntent


class S3FileStorageIntent(FileStorageIntent):

    def __init__(self, from_path, to_path, bucket):
        super(S3FileStorageIntent, self).__init__(from_path, to_path)
        self.bucket = bucket

    def store(self):
        k = Key(self.bucket)
        k.key = self.to_path
        k.set_contents_from_filename(self.from_path)


class S3Storage(Storage):

    def __init__(self, bucket_name):
        self.connection = S3Connection(os.environ.get('AWS_ACCESS_KEY_ID'),
                                       os.environ.get('AWS_SECRET_ACCESS_KEY'))
        self.bucket = self.connection.create_bucket(bucket_name)

    def storage_intent(self, from_path, to_path):
        return S3FileStorageIntent(from_path, to_path, self.bucket)
