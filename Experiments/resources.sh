#!/bin/bash

# Create nested repositories
mkdir -p resources/dataset

# URL of the file to download
file_url="https://dl.fbaipublicfiles.com/clevr/CLEVR_v1.0_no_images.zip"

# Download the file using wget
wget -P resources/dataset "$file_url"

unzip resources/dataset/CLEVR_v1.0_no_images.zip -d resources/dataset

rm resources/dataset/CLEVR_v1.0_no_images.zip