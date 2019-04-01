'''
This file will define a function that will launch an EC2 instance.. 

'''

import boto3

userdata = '''#!/bin/bash
cd home/ubuntu

pip install librosa

sudo -u ubuntu mkdir results

git clone https://github.com/MathiasDarr/KerasStyleTransfer.git 
python KerasStyleTransfer/downloadS3.py 'base_image.jpg' base_image.jpg
python KerasStyleTransfer/downloadS3.py 'style_image.jpg' style_image.jpg
python KerasStyleTransfer/downloadS3.py 'bootstrap.sh' bootstrap.sh

sudo python KerasStyleTransfer/test_keras_import.py > keras_import.txt

sudo bootstrap.sh



'''

testdata='''#!/bin/bash

cd /home/ubuntu
sudo pip install librosa
sudo pip install tensorflow
sudo pip install keras
sudo pip freeze | grep "keras" > /home/ubuntu/keras.txt
git clone https://github.com/MathiasDarr/KerasStyleTransfer.git 
sudo bash KerasStyleTransfer/test_keras_import.py > keras_import.txt

'''

# sudo -u ubuntu bash /home/ubuntu/bootstrap.sh > /home/ubuntu/bootstrap.log
#python KerasStyleTransfer/styletransfer.py style_image.jpg base_image.jpg results/myimage
# sudo -u ubuntu



def launchEC2():

    REGION = 'us-west-2' # region to launch instance.

    INSTANCE_TYPE = 't2.micro'      # Test with the micro
    #INSTANCE_TYPE = 'g3s.xlarge' # instance type to launch.
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
        UserData = testdata
    )

AmazonUserData = '''#!/bin/bash

cd home/ubuntu

sudo mkdir anaconda
cd anaconda
sudo wget https://repo.continuum.io/archive/Anaconda3-5.0.1-Linux-x86_64.sh
sudo bash Anaconda3-5.0.1-Linux-x86_64.sh
export python3=/anaconda/anaconda3/bin/python
cd /home/ubuntu

sudo mkdir results

git clone https://github.com/MathiasDarr/KerasStyleTransfer.git 
$python3 KerasStyleTransfer/downloadS3.py 'base_image.jpg' base_image.jpg
$python3 KerasStyleTransfer/downloadS3.py 'style_image.jpg' style_image.jpg

sudo /anaconda/anaconda3/bin/pip install --upgrade pip

sudo /anaconda/anaconda3/bin/pip install tensorflow
sudo /anaconda/anaconda3/bin/pip install keras

$python3 KerasStyleTransfer/styletransfer.py style_image.jpg base_image.jpg results/myimage

'''


AmazonLinuxUserData = '''#!/bin/bash

'''


def launchAmazonLinuxEC2():

    REGION = 'us-west-2' # region to launch instance.

    #INSTANCE_TYPE = 't2.micro'      # Test with the micro
    INSTANCE_TYPE = 'g3s.xlarge' # instance type to launch.
    AMI = 'ami-0283132d7b60d70b9'

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
        UserData = AmazonUserData
    )

