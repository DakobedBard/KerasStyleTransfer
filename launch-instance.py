'''
This script will be used to launch EC2 instances with the required IAM role.. 

Later on in development I hope to have this be run from a Lamda function.. 

I have to determine the differences between instance profiel arn vs role arn 

EC2 instance profile 


This is the image arn.. 

arn:aws:iam::710339184759:role/EC2-S3-SES



'''
import boto3

ec2 = boto3.resource('ec2', region_name='us-west-2')
ec2.create_instances(ImageId='ami-1e299d7e',
                     InstanceType='g3s.xlarge',
                     MinCount=1, MaxCount=1,
                     SecurityGroupIds=['Mysecuritygroup'],
                     KeyName='ec2-keypair',
                     IamInstanceProfile={
                            'Arn': 'arn:aws:iam::123456789012:instanceprofile/LaunchedImageFromBoto3'
                     })
