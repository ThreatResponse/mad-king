import boto3

class Actions(object):
        def __init__(self, region, instance):
            self.client = boto3.client('ec2', region)
            self.instance = instance

        def burn_instance(self):
            response = self.client.terminate_instances(
                DryRun=True,
                InstanceIds=[
                    self.instance
                ]
            )
            return response

        def stop_instance(self):
            response = self.client.stop_instances(
                DryRun=True,
                InstanceIds=[
                    self.instance
                ]
            )
            return response

class fullMadness(object):
    def __init__(self, inventory):
        self.inventory = inventory

    def burn_them_all(self):
        for region in self.inventory:
            for instance in self.inventory[region]:
                action = Actions(region, instance['instance_id'])
                try:
                    action.burn_instance()
                except:
                    pass
