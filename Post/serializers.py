from rest_framework import serializers

from .models import Tashxis
from User.serializers import UserSer, BemorSer


class TashxisSer(serializers.ModelSerializer):
    class Meta:
        model = Tashxis
        fields = '__all__'
    

class TashxisGetSer(serializers.ModelSerializer):
    user = UserSer()
    bemor = BemorSer()
    class Meta:
        model = Tashxis
        fields = ['id', 'user', 'bemor', 'sick', 'date', 'created_at', 'narx', 'tuladi', 'qoldi']
