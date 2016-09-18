import boto3

class Connect(object):
    def __init__(self, region='us-west-2', service='ec2'):
        self.region = region
        self.service = service

        try:
          self.client = boto3.client(service,region)
        except:
          raise StandardError(
            "No AWS Credentials could be found."
          )

class Region(object):
  def __init__(self):
    self.client = Connect().client

  def get_all(self):
    availRegions = []
    regions = self.client.describe_regions()
    for region in regions['Regions']:
        availRegions.append(region['RegionName'])
    return availRegions

class Instance(object):
  def __init__(self):
    self.client = Connect().client

  def get_running_by_region(self, region):
    inventory = []

    reservations = Connect(region).client.describe_instances(
            Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
            )['Reservations']

    for reservation in reservations:
      for instance in reservation['Instances']:
          instance_data = self.__extract_data(instance)
          instance_data['region'] = region
          inventory.append(instance_data)

    return inventory

  def __extract_data(self, instance):
    return dict(
      public_ip_address = instance.get('PublicIpAddress', None),
      instance_id = instance['InstanceId'],
      launch_time = instance['LaunchTime'],
      platform = instance.get('Platform', None),
      vpc_id = instance['VpcId'],
      ami_id = instance['ImageId'],
      volume_ids = [ bdm['Ebs']['VolumeId'] for bdm in instance.get('BlockDeviceMappings', [] ) ],
      )

  def get_all_running(self):
    inventory = {}

    for region in Region().get_all():
      inventory[region] = self.get_running_by_region(region)

    return inventory

class Who(object):
    def __init__(self):
        self.client = boto3.client('sts')
        self.identity = self.client.get_caller_identity()


class CloudTrail(object):
    def __init__(self):
        self.client = boto3.client('cloudtrail', 'us-west-2')

    def get_trails(self):
        response = self.client.describe_trails(
            includeShadowTrails=True
        )
        return response

    def disrupted(self, trail, trailArn):

        response = self.client.get_trail_status(
            Name=trailArn
        )

        description = self.client.describe_trails(
            trailNameList=[
                trail
            ]
        )

        if response['IsLogging'] == False or description['trailList'][0]['KmsKeyId'] != None:
            return True
        else:
            return False
