# flask_s3_uploads/__init__.py

from flask import Flask, render_template, request, redirect
from werkzeug.utils import secure_filename
import boto3
application = app =Flask(__name__)
application.config.from_object("config")

from config import S3_KEY, S3_SECRET

s3 = boto3.client(
    's3',
    # Hard coded strings as credentials, not recommended.
    aws_access_key_id=S3_KEY,
    aws_secret_access_key=S3_SECRET
)


ALLOWED_EXTENSIONS = set(['jpg', 'jpeg'])


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

    except Exception as e:
        # This is a catch all exception, edit this part to fit your needs.
        print("Something Happened: ", e)
        return e

    return "{}{}".format(app.config["S3_LOCATION"], file.filename)




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@app.route("/", methods=["GET" ,"POST"])
def uploadfile():

	# A
    if "user_file" not in request.files:
        return "No user_file key in request.files"

	# B
    file    = request.files["user_file"]

    """
        These attributes are also available

        file.filename               # The actual name of the file
        file.content_type
        file.content_length
        file.mimetype

    """

	# C.
    if file.filename == "":
        return "Please select a file"

	# D.
    if file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output   	  = upload_file_to_s3(file, app.config["S3_BUCKET"])
        return str(output)

    else:
        return redirect("/")



'''
A. We check the request.files object for a user_file key. (user_file is the name of the file input on our form). If it’s not there, we return an error message.

B. If the key is in the object, we save it in a variable called file.

C. We check the filename attribute on the object and if it’s empty, it means the user sumbmitted an empty form, so we return an error message.

D. Finally we check that there is a file and that it has an allowed filetype (this is what the allowed_file function does, you can check it out in the flask docs).

If both tests pass, we sanitize the filename using the secure_filename helper function provided by the werkzeurg.security module. Next, we upload the file to our s3 bucket using our own helper function, we store the return value (ie the generated presigned url for the file) in a variable o called output. We end by returning the generated url to the user.

Note: if one of the tests fail, we just redirect the user to the home page, similar to a refresh



'''
