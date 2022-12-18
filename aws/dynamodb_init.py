import time
from turtle import title
import boto3
from botocore.client import logger
from botocore.exceptions import ClientError


class AwsDynamodbOperations:

    @staticmethod
    def create_table():
        dynamodb = boto3.resource('dynamodb')

        # Create the DynamoDB table.
        table = dynamodb.create_table(
            TableName='tasks',
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'task_name',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                },
                {
                    'AttributeName': 'task_name',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5
            }
        )

        print('initializing table..!')

        # Wait until the table exists.
        table.wait_until_exists()

        # Print out some data about the table.
        print(table.item_count)

    @staticmethod
    def save(data):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('tasks')
        data["id"] = int(time.time())
        table.put_item(Item=data)

    @staticmethod
    def delete(data):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('tasks')
        table.delete_item(
            Key={
                'id': int(data['id']),
                'task_name': data['task_name']
            }
        )

    @staticmethod
    def update(data):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('tasks')
        table.update_item(
            Key={
                'id': int(data['id']),
                'task_name': data['task_name']
            },
            UpdateExpression='SET task_duration = :val1, task_status = :val2, task_priority = :val3',
            ExpressionAttributeValues={
                ':val1': data['task_duration'],
                ':val2': data['task_status'],
                ':val3': data['task_priority']
            }
        )
        response = table.get_item(
            Key={
                'id': int(data['id']),
                'task_name': data['task_name']
            }
        )
        items = response['Item']
        return items

    @staticmethod
    def query_all():
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('tasks')
            response = table.scan()
            items = response['Items']
            return items
        except ClientError as err:
            print(
                "Couldn't update movie %s in table %s. Here's why: %s: %s",
                title, "tasks",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise

    @staticmethod
    def query_by_id_name(data):
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('tasks')
        response = table.get_item(
            Key={
                'id': int(data['id']),
                'task_name': data['task_name']
            }
        )
        item = response['Item']
        return item
