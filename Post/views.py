from functools import partial
from django.shortcuts import render
from django.db.models import Q, F, Count, Sum, Min, Max
from django.utils import timezone
from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser

from .models import Tashxis
from .serializers import TashxisSer, TashxisGetSer, TezTashxisSer
from User.models import Bemor


class TashxisList(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    def get(self, request):
        tashxis = Tashxis.objects.all()
        serializer = TashxisGetSer(tashxis, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TashxisSer(data=request.data)
        if serializer.is_valid():
            a = request.data.get('narx', None)
            b = request.data.get('tuladi', None)
            t = serializer.save()
            if a and b:
                t.qoldi = t.narx-t.tuladi
                t.save()
            elif a:
                t.qoldi = t.narx
                t.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class TashxisDetail(APIView):
    parser_classes = (MultiPartParser, JSONParser)
    def get(self, request, id):
        tashxis = Tashxis.objects.get(id=id)
        serializer = TashxisSer(tashxis)
        return Response(serializer.data)

    def patch(self, request, id):
        tashxis = Tashxis.objects.get(id=id)
        serializer = TashxisSer(tashxis, data=request.data, partial=True)
        if serializer.is_valid():
            a = request.data.get('narx', None)
            b = request.data.get('tuladi', None)
            t = serializer.save()
            if a and b:
                t.qoldi = t.narx-t.tuladi
                t.save()
            elif a:
                t.qoldi = t.narx
                t.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request, id):
        xodim = Tashxis.objects.filter(id=id).first()
        xodim.delete()
        return Response({'message': 'Deleted'})


# class TezTashxisList(APIView):
#     parser_classes = (MultiPartParser, JSONParser)
#     def get(self, request):
#         tashxis = Tashxis.objects.all()
#         serializer = TezTashxisSer(tashxis, many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = TezTashxisSer(data=request.data)
#         if serializer.is_valid():
#             # a = request.data.get('narx', None)
#             # b = request.data.get('tuladi', None)
#             serializer.save()
#             # if a and b:
#             #     t.qoldi = t.narx-t.tuladi
#             #     t.save()
#             # elif a:
#             #     t.qoldi = t.narx
#             #     t.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)


class TezTashxisList(APIView):
    def post(self, request):
        serializer = TezTashxisSer(data=request.data)
        if serializer.is_valid():
            bemor_data = serializer.validated_data.get('bemor')
            bemor, created = Bemor.objects.get_or_create(
                first_name=bemor_data.get('first_name'),
            )
            if created:
                serializer.validated_data['bemor'] = bemor
            else:
                serializer.validated_data['bemor'] = bemor
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)