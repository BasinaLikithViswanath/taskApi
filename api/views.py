from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from aws.dynamodb_init import AwsDynamodbOperations
from rest_framework import status

awsDynamodbOperations = AwsDynamodbOperations()


class TaskListView(APIView):
    @staticmethod
    def get(request):
        return Response(awsDynamodbOperations.query_all())

    @staticmethod
    def post(request):
        data = JSONParser().parse(request)
        awsDynamodbOperations.save(data)
        return Response(data)


class TaskDetailView(APIView):

    @staticmethod
    def get(request):
        data = JSONParser().parse(request)
        return Response(awsDynamodbOperations.query_by_id_name(data))

    @staticmethod
    def delete(request):
        data = JSONParser().parse(request)
        awsDynamodbOperations.delete(data)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def put(request):
        data = JSONParser().parse(request)
        return Response(awsDynamodbOperations.update(data))
