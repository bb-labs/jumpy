#!/bin/sh

zip -r ./package.zip .

aws lambda create-function \
    --function-name numpy-endpoint-2 \
    --runtime python3.7 \
    --zip-file fileb://package.zip \
    --handler numpy-endpoint-2.lambda_handler \
    --role arn:aws:iam::718734850255:role/service-role/admin
