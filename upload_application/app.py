import os
from flask import Flask, render_template, request
import boto3

from config import S3_KEY, S3_SECRET, S3_BUCKET

app = Flask(__name__)

UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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


    upload_file_to_s3(sf,S3_BUCKET)
    upload_file_to_s3(f,S3_BUCKET)


    return render_template('index.html')



def allowed_file(filename):
    return '.' in filename and \
       filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




def upload_file_to_s3(file, bucket_name, acl="public-read"):

    try:

        s3.upload_fileobj(
            file,
            bucket_name,
            file.filename,
            ExtraArgs={
                "ACL": acl,
                "ContentType": file.content_type
            }
        )

        print("I worked!")

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)
