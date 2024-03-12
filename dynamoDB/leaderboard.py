import boto3

def create_leaderboard_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    table = dynamodb.create_table(
        TableName='Leaderboard',
        KeySchema=[
            {
                'AttributeName': 'UserID',
                'KeyType': 'HASH'  # Primary key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'UserID',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

if __name__ == '__main__':
    leaderboard_table = create_leaderboard_table()
    print("Table status:", leaderboard_table.table_status)
