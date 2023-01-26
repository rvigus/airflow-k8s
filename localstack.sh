docker run --rm -it -p 4566:4566 -p 4510-4559:4510-4559 localstack/localstack

aws_local="aws --endpoint-url=http://localhost:4566 --profile localstack"

$aws_local s3 mb s3://data


