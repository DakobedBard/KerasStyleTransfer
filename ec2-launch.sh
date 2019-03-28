#!/usr/bin/env bash

source activate tensorflow_p36

git clone https://github.com/JasonHeyward/KerasStyleTransfer.git

mkdir KerasStyleTransfer/result/


# -> read in the images from s3: ... 

python styletransfer.py the-scream.jpg glacier-peak.jpg results/myimage


# heyward-style-transfer-images This is where I will save output images..

# Figure out how to save the model and apply it to a new image.. 
# Figure out how to adjust the parameters 

