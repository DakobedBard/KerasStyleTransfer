'''
This file will define a function that will launch an EC2 instance.. 

'''

import boto3

userdata = '''#!/bin/bash
git clone https://github.com/MathiasDarr/KerasStyleTransfer.git 
source activate tensorflow_p36


python KerasStyleTransfer/downloadS3.py 'base_image.jpg' base_image.jpg
python KerasStyleTransfer/downloadS3.py 'style_image.jpg' style_image.jpg

mkdir results

python KerasStyleTransfer/styletransfer.py style_image.jpg base_image.jpg results/myimage

'''

def launchEC2():

    REGION = 'us-west-2' # region to launch instance.
    AMI = 'ami-01a4e5be5f289dd12'
    # matching region/setup amazon linux ami, as per:
    # https://aws.amazon.com/amazon-linux-ami/
    INSTANCE_TYPE = 'g3s.xlarge' # instance type to launch.

    ec2 = boto3.resource('ec2', region_name='us-west-2')

    instances = ec2.create_instances(
        ImageId=AMI,
        MinCount=1,
        MaxCount=1,
        KeyName='gpu-style',
        InstanceInitiatedShutdownBehavior='terminate',
        InstanceType=INSTANCE_TYPE
    )



def launchTestEC2():

    REGION = 'us-west-2' # region to launch instance.

    INSTANCE_TYPE = 't2.micro'
    AMI = 'ami-01a4e5be5f289dd12'

    ec2 = boto3.resource('ec2', region_name=REGION)
    instances = ec2.create_instances(
        ImageId=AMI,
        MinCount=1,
        MaxCount=1,
        KeyName='gpu-style',
        InstanceInitiatedShutdownBehavior='terminate',
        IamInstanceProfile={'Name':'S3fullaccess'},
        InstanceType=INSTANCE_TYPE,
        SecurityGroupIds=['sg-03915a624fb5bf7bd'],
        UserData = userdata
    )

