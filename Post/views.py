from functools import partial
from django.shortcuts import render
from django.db.models import Q, F, Count, Sum, Min, Max
from django.utils import timezone
from datetime import datetime, timedelta

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser

from .models import Tashxis
from .serializers import TashxisSer, TashxisGetSer


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