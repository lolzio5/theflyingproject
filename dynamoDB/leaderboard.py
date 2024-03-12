import boto3

def create_leaderboard_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    table = dynamodb.create_table(
        TableName='Leaderboard',
        KeySchema=[
            {
                'AttributeName': 'UserID',
                'KeyType': 'S'  # Primary key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'PlayedTime',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'TimeAtTriggerBox1',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'TimeAtTriggerBox2',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'TimeAtTriggerBox3',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table

def update_leaderboard(dynamodb, json_data):
    is_leaderboard_message = 0
    
    leaderboard_dict = json_data.load()
    if leaderboard_dict.get("leaderboard"):
        player = leaderboard_table.get("player")
        is_leaderboard_message = 1
        
        if dynamodb:
            table = dynamodb.Table('Leaderboard')
            
            table.update_item(
                            key={
                                'UserID':player,
                            },
                            UpdateExpression='SET PlayedTime=:val1',
                            ExpressionAttributeValues={
                                ':val1': leaderboard_dict.get("PlayedTime")
                            }
                        )
            for i in range(3):
                    if leaderboard_dict.get("TimeAtTriggerBox" + str(i)):
                        table.update_item(
                            key={
                                'UserID':player,
                            },
                            UpdateExpression='SET TimeAtTriggerBox'+str(i)+'= :val1',
                            ExpressionAttributeValues={
                                ':val1': leaderboard_dict.get("TimeAtTriggerBox"+str(i))
                            }
                        )
    return is_leaderboard_message

if __name__ == '__main__':
    leaderboard_table = create_leaderboard_table()
    print("Table status:", leaderboard_table.table_status)
