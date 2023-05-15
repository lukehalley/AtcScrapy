import boto3


def InitDynamoDB():

    # Creating the DynamoDB Client
    DynamodbClient = boto3.client('dynamodb', region_name="eu-west-1")

    # Creating the DynamoDB Table Resource
    DynamodbResource = boto3.resource('dynamodb', region_name="eu-west-1")

    return DynamodbResource, DynamodbClient

