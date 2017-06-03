from __future__ import print_function # Python 2/3 compatibility
import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)

dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table = dynamodb.Table('Matches')

def add_match(player_id, match_id, info): 
    response = table.put_item(
        Item={
            'player_id': str(player_id),
            'match_id': str(match_id), 
            'info': info
        }
    )

    print("PutItem succeeded:")
    print(json.dumps(response, indent=4, cls=DecimalEncoder))


def check_match(player_id, match_id):
    response = table.query(
            KeyConditionExpression=Key('player_id').eq('123') & Key('match_id').eq('321231')
                    )
    return bool(len(response['Items']))
