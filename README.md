# KerasStyleTransfer

In this project I have deployed a Flask application to AWS Elastic Beanstalk.  The application allows a user to upload two images and to perform style transfer using the Keras deep learning library.  In order to do this, I used the boto3 python library to launch AWS EC2 instances to perform the computations, and then email the resulting style transered image to the user.  
