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
          InstanceType=INSTANCE_TYPE
     )


def generate_key_pair():

    '''
    Generate a key-pair
    '''

    ec2 = boto3.resource('ec2')

    # create a file to store the key locally
    outfile = open('ec2-keypair.pem','w')

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName='ec2-keypair')

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)


def delete_key_pair():
     '''
     Delete a key pair
     '''

     ec2 = boto3.client('ec2')
     response = ec2.delete_key_pair(KeyName='ec2-keypair')
     print(response)

