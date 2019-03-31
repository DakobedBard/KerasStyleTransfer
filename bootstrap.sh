#!/bin/bash


source activate tensorflow_p36
env | grep -e CONDA -e PS1 > env.txt

python KerasStyleTransfer/styletransfer.py style_image.jpg base_image.jpg results/myimage

