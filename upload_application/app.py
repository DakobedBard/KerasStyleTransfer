import os
from flask import Flask, render_template, request
import boto3
import botocore
from config import S3_KEY, S3_SECRET, S3_BUCKET

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['S3_LOCATION'] = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])

s3 = boto3.client(
    's3',
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)




@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['base_image']
    f = os.path.join(app.config['UPLOAD_FOLDER'], 'base_image.jpg')
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    file.save(f)

    style_file = request.files['style_image']
    sf = os.path.join(app.config['UPLOAD_FOLDER'], 'style_image.jpg')
    # add your custom code to check that the uploaded file is a valid image and not a malicious file (out-of-scope for this post)
    style_file.save(sf)

    cwd = os.getcwd()

    full_style_path = os.path.join(cwd,sf)
    full_base_path = os.path.join(cwd,f)
    
    style_upload = upload_S3(full_style_path,S3_BUCKET,'style_image.jpg')
    base_upload =  upload_S3(full_base_path,S3_BUCKET,'base_image.jpg')


    print(style_upload)


    return render_template('index.html')



def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


'''
The boto3 method upload_fileobj expects a fileobj

upload_file

upload_fileobj

'''



def upload_S3(filepath, bucket, filename):
    s3_resource = boto3.resource('s3')
    try:
        s3_resource.meta.client.upload_file(filepath,bucket,filename)    

        print("I worked!")

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e
    return "{}{}".format(app.config["S3_LOCATION"], filename)



def download_S3():
    '''
    This method will be called from the EC2 instance.. 
    '''
    s3_resource = boto3.resource('s3')
    try:
        s3_resource.Bucket(S3_BUCKET).download_file('base_image.jpg', 'S3_image.jpg')
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("The object does not exist.")
        else:
            raise



'''

You can name your objects by using standard file naming conventions. You can use any valid name. In this article, you’ll look at a more specific case that helps you understand how S3 works under the hood.

If you’re planning on hosting a large number of files in your S3 bucket, there’s something you should keep in mind. If all your file names have a deterministic prefix that gets repeated for every file, such as a timestamp format like “YYYY-MM-DDThh:mm:ss”, then you will soon find that you’re running into performance issues when you’re trying to interact with your bucket.

This will happen because S3 takes the prefix of the file and maps it onto a partition. The more files you add, the more will be assigned to the same partition, and that partition will be very heavy and less responsive.

What can you do to keep that from happening?

The easiest solution is to randomize the file name. You can imagine many different implementations, but in this case, you’ll use the trusted uuid module to help with that. To make the file names easier to read for this tutorial, you’ll be taking the first six characters of the generated number’s hex representation and concatenate it with your base file name.

The helper function below allows you to pass in the number of bytes you want the file to have, the file name, and a sample content for the file to be repeated to make up the desired file size:


'''