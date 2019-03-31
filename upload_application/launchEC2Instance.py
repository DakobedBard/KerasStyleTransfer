'''
This file will define a function that will launch an EC2 instance.. 

'''

import boto3

userdata = '''#!/bin/bash
cd home/ubuntu

sudo -u ubuntu mkdir results

git clone https://github.com/MathiasDarr/KerasStyleTransfer.git 
python KerasStyleTransfer/downloadS3.py 'base_image.jpg' base_image.jpg
python KerasStyleTransfer/downloadS3.py 'style_image.jpg' style_image.jpg
python KerasStyleTransfer/downloadS3.py 'bootstrap.sh' bootstrap.sh

sudo -u ubuntu bash /home/ubuntu/bootstrap.sh > /home/ubuntu/bootstrap.log

'''

#python KerasStyleTransfer/styletransfer.py style_image.jpg base_image.jpg results/myimage
# sudo -u ubuntu



def launchEC2():

    REGION = 'us-west-2' # region to launch instance.

    #INSTANCE_TYPE = 't2.micro'      # Test with the micro
    INSTANCE_TYPE = 'g3s.xlarge' # instance type to launch.
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


