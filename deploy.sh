#!/bin/sh

# Don't do this ever --- 
# aws_access_key_id = AKIA2OV7PPDHV2G7GWEF
# aws_secret_access_key = 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

mkdir -p ~/.aws

echo -e "[default]\nregion = us-west-2\noutput = json" >~/.aws/config
echo -e "[default]\naws_access_key_id = $1\naws_secret_access_key = $2" >~/.aws/credentials

# aws lambda create-function \
#     --function-name numpy-endpoint-2 \
#     --runtime python3.7 \
#     --zip-file fileb://package.zip \
#     --handler numpy-endpoint-2.lambda_handler \
#     --role arn:aws:iam::718734850255:role/service-role/admin
