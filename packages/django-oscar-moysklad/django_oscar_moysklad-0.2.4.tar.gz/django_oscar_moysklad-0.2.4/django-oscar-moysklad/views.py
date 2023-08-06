from django.shortcuts import render

# Create your views here.
from rest_framework import status, generics, serializers
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import APIView
#
# # from synchroniser.load.stock.stock import StockSyncLoadTask
# from .synchronizer.tasks import initial_task
#
#
# class SyncProductFolder(APIView):
#
#     serializer_class = serializers.EmptySerializer
#
#     def get(self, request, format=None):
#         raise MethodNotAllowed('GET')
#
#     def post(self, request, format=None):
#         initial_task()
#         # product_update_task()
#         # StockSyncLoadTask().execute()
#         # sync_product_folder()
#         return Response({
#             'status': 'Success',
#         })

