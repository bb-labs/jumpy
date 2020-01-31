#!/bin/sh

# Create AWS profile from user passed keys
mkdir -p ~/.aws

echo -e "[default]\nregion = us-west-2\noutput = json" >~/.aws/config
echo -e "[default]\naws_access_key_id = $1\naws_secret_access_key = $2" >~/.aws/credentials

# Get the JumPy repository
git clone https://github.com/bb-labs/jumpy.git

# Zip the files together
cd jumpy/src/back
cp -r /var/lang/lib/python3.7/site-packages/numpy .
zip -r package.zip .

# Check out the size
ls -lah

# Check if the lambda exists
aws lambda get-function \
    --function-name numpy-endpoint \
    --output text \
    &>response

# If it doesn't, make it
if grep -q "An error occurred" response; then
    aws lambda create-function \
        --function-name numpy-endpoint \
        --runtime python3.7 \
        --zip-file fileb://package.zip \
        --handler lambda_function.lambda_handler \
        --role arn:aws:iam::718734850255:role/service-role/admin
# Otherwise just update it
else
    aws lambda update-function-code \
        --function-name numpy-endpoint \
        --zip-file fileb://package.zip
fi
