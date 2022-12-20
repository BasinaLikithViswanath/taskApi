import time
import boto3
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from taskApi import settings


class AwsDynamodbOperations:

    CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

    @staticmethod
    def flush():
        if 'tasks' in cache:
            cache.delete('tasks')

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

    def save(self, data):
        dynamodb = boto3.resource(
            'dynamodb',
            region_name='us-east-1'
        )
        key = {
            'id': int(data['id']),
            'task_name': data['task_name']
        }
        table = dynamodb.Table('tasks')
        data["id"] = int(time.time())
        table.put_item(Item=data)

        self.flush()
        cache.set(key, data, self.CACHE_TTL)

    def delete(self, data):
        dynamodb = boto3.resource(
            'dynamodb',
            region_name='us-east-1'
        )
        key = {
            'id': int(data['id']),
            'task_name': data['task_name']
        }
        table = dynamodb.Table('tasks')
        table.delete_item(
            Key=key
        )

        self.flush()
        if key in cache:
            cache.delete(key)

    def update(self, data):
        dynamodb = boto3.resource(
            'dynamodb',
            region_name='us-east-1'
        )
        key = {
            'id': int(data['id']),
            'task_name': data['task_name']
        }
        table = dynamodb.Table('tasks')
        table.update_item(
            Key=key,
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

        self.flush()
        if key in cache:
            cache.set(key, items, timeout=self.CACHE_TTL)

        return items

    def query_all(self):

        if 'tasks' in cache:
            return cache.get('tasks')

        dynamodb = boto3.resource(
            'dynamodb',
            region_name='us-east-1'
        )
        table = dynamodb.Table('tasks')
        response = table.scan()
        items = response['Items']

        cache.set('tasks', items, self.CACHE_TTL)
        return items

    def query_by_id_name(self, data):

        key = {
            'id': int(data['id']),
            'task_name': data['task_name']
        }

        if key in cache:
            return cache.get(key)

        dynamodb = boto3.resource(
            'dynamodb',
            region_name='us-east-1'
        )
        table = dynamodb.Table('tasks')
        response = table.get_item(Key=key)
        item = response['Item']

        cache.set(key, item, self.CACHE_TTL)
        return item
