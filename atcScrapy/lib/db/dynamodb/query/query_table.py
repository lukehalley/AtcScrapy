
from boto3.dynamodb.conditions import Key

from atcScrapy.lib.db.dynamodb.setup.setup_Init import InitDynamoDB


def QuerySigTable(HashedSignature):

    # Init DynamoDB Client
    DynamodbResource, DynamodbClient = InitDynamoDB()

    # Init Table Object
    DynamodbTable = DynamodbResource.Table("atc_sig_db")

    # Execute Query
    QueryResponse = DynamodbTable.query(
        IndexName='hashedSignature-index',
        KeyConditionExpression=Key('hashedSignature').eq(HashedSignature)
    )

    return QueryResponse["Items"]