#!/bin/sh

root_dir=$(pwd)

echo $root_dir
echo ~

# pip install numpy
# cp -r /var/lang/lib/python3.6/site-packages/numpy $root_dir/jumpy

# cd $root_dir/jumpy/deploy
# mv ~/.terraform .

# terraform init

terraform plan \
-out=numpy-deployment-plan \
-input=false \
-var="lambda_path=$root_dir/jumpy" \

# terraform apply \
# -input=false \
# numpy-deployment-plan
