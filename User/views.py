from django.shortcuts import render
from django.db.models import Q, F, Sum, Min, Max

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, JSONParser
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSer, BemorSer, ChangePasswordSerializer, BemorGetSer
from .models import User, Bemor
from Post.models import Tashxis


class ChangePasswordView(APIView):
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = self.request.user
            old_password = serializer.data.get('old_password')
            new_password = serializer.data.get('new_password')

            if not user.check_password(old_password):
                return Response({'detail': 'Old password is incorrect.'})

            user.set_password(new_password)
            user.save()
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)
            return Response({'detail': 'Password changed successfully.',
                             'access_token': access,
                             'refresh_token': str(refresh)
                             })

        return Response(serializer.errors)


class Userdetail(APIView):
    # permission_classes = [IsAuthenticated,]
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            ser = UserSer(user)
            if Tashxis.objects.filter(user=user):
                tashxis = Tashxis.objects.filter(user=user)
                c = {}
                sum_narx = tashxis.aggregate(Sum('narx'))
                sum_tuladi = tashxis.aggregate(Sum('tuladi'))
                sum_qoldi = tashxis.aggregate(Sum('qoldi'))
                c['tuliq_narx'] = sum_narx['narx__sum']
                c['tuliq_tuladi'] = sum_tuladi['tuladi__sum']
                c['tuliq_qoldi'] = sum_qoldi['qoldi__sum']
                c['tashxis'] = Tashxis.objects.filter(user=user).count()
                d = []
                for x in tashxis:
                    found = False
                    for item in d:
                        if item['tashxislar'] == x.sick:
                            # item['tashxislar'] = x.sick
                            item['narx'] += x.narx
                            item['tuladi'] += x.tuladi
                            item['qoldi'] += x.qoldi
                            item['sum_tashxis'] += 1
                            found = True
                            break
                    if not found:
                        d.append({'tashxislar': x.sick, 'narx': x.narx,
                                  'tuladi': x.tuladi, 'qoldi': x.qoldi,
                                  'sum_tashxis': 1})
                return Response({'data': ser.data,
                                 'all_statistic': c,
                                 'statistic': d})
            return Response({'data': ser.data,
                                'all_statistic': None,
                                'statistic': None})
        except:
            return Response({'message': 'Not found'})
    
    def patch(self, request, id):
        user = User.objects.filter(id=id).first()
        ser = UserSer(data=request.data, instance=user, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
    def delete(self, request, id):
        user = User.objects.filter(id=id).first()
        user.delete()
        return Response({'message': 'User deleted successfully.'})


class SignUp(APIView):
    parser_classes = [MultiPartParser, JSONParser]
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        user = User.objects.all()
        ser = UserSer(user, many=True)
        return Response(ser.data)

    def post(self, request):
        ser = UserSer(data=request.data)
        if ser.is_valid():
            status_d = ser.validated_data.get('status')
            if status_d in ['Direktor']:
                if User.objects.filter(status=status_d).exists():
                    return Response({'message': f'Bunday {status_d} Tayinlab Bulingan'})
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)

class BemorList(APIView):
    parser_classes = [MultiPartParser, JSONParser]
    def get(self, request):
        xodim = Bemor.objects.all()
        ser = BemorGetSer(xodim, many=True)
        return Response(ser.data)
    
    def post(self, request):
        ser = BemorSer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)


class BemorDetail(APIView):
    parser_classes = [MultiPartParser, JSONParser]
    def get(self, request, id):
        try:
            bemor = Bemor.objects.get(id=id)
            ser = BemorSer(bemor)
            if Tashxis.objects.filter(bemor=bemor):
                tashxis = Tashxis.objects.filter(bemor=bemor)
                c = {}
                sum_narx = tashxis.aggregate(Sum('narx'))
                sum_tuladi = tashxis.aggregate(Sum('tuladi'))
                sum_qoldi = tashxis.aggregate(Sum('qoldi'))
                sum_tash = Tashxis.objects.filter(bemor=bemor).count()
                c['sum_narx'] = sum_narx['narx__sum']
                c['sum_tuladi'] = sum_tuladi['tuladi__sum']
                c['sum_qoldi'] = sum_qoldi['qoldi__sum']
                c['sum_tashxislar'] = sum_tash
                d = []
                for x in tashxis:
                    found = False
                    for item in d:
                        if item['tashxislar'] == x.sick:
                            # item['tashxislar'] = x.sick
                            item['narx'] += x.narx
                            item['tuladi'] += x.tuladi
                            item['qoldi'] += x.qoldi
                            item['sum_tashxis'] += 1
                            found = True
                            break
                    if not found:
                        d.append({'tashxislar': x.sick, 'narx': x.narx,
                                  'tuladi': x.tuladi, 'qoldi': x.qoldi,
                                  'sum_tashxis': 1,})
                return Response({'data': ser.data,
                                 'all_statistic': c,
                                 'statistic': d})
            return Response({'data': ser.data,
                                 'all_statistic': None,
                                 'statistic': None})
        except:
            return Response({'message': 'Not found'})
    
    def patch(self, request, id):
        xodim = Bemor.objects.filter(id=id).first()
        ser = BemorSer(xodim, data=request.data, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)
    
    def delete(self, request, id):
        xodim = Bemor.objects.filter(id=id).first()
        xodim.delete()
        return Response({'message': 'Deleted'})
