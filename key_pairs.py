import boto3

def delete_key_pair():
     '''
     Delete a key pair
     '''

     ec2 = boto3.client('ec2')
     response = ec2.delete_key_pair(KeyName='ec2-keypair')
     print(response)

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
