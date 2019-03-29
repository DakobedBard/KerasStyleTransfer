""" Script to launch EC2 instance..."""
import boto3

def launch_instance():

     REGION = 'us-west-2' # region to launch instance.
     AMI = 'ami-01a4e5be5f289dd12'
     # matching region/setup amazon linux ami, as per:
     # https://aws.amazon.com/amazon-linux-ami/
     INSTANCE_TYPE = 'g3s.xlarge' # instance type to launch.


     ec2 = boto3.resource('ec2')

     instances = ec2.create_instances(
          ImageId=AMI,
          MinCount=1,
          MaxCount=1,
          KeyName='ec2-keypair',
          IamInstanceProfile={'Name':'Lamda-LaunchEC2'},
          InstanceType=INSTANCE_TYPE
     )
