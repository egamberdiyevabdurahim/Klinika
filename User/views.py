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
            return Response(ser.data)
        except:
            return Response({'message': 'Not found'})
    
    def patch(self, request, id):
        user = User.objects.filter(id=id).first()
        ser = UserSer(data=request.data, instance=user, partial=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data)
        return Response(ser.errors)


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
            xodim = Bemor.objects.get(id=id)
            ser = BemorSer(xodim)
            return Response({'data': ser.data})
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
