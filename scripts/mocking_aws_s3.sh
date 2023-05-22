#! /bin/sh

aws s3 mb s3://example-bucket --endpoint-url=http://localstack:4566
aws s3 cp /data/audio/test.mp3 s3://example-bucket/audio/test.mp3 --endpoint-url=http://localstack:4566
