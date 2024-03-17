from rest_framework import serializers

from .models import Tashxis
from User.serializers import UserSer, BemorSer
from User.models import Bemor


class TashxisSer(serializers.ModelSerializer):
    class Meta:
        model = Tashxis
        fields = '__all__'
    

class TashxisGetSer(serializers.ModelSerializer):
    bemor = BemorSer()
    class Meta:
        model = Tashxis
        fields = ['id', 'bemor', 'diagnoz', 'tashxis', 'date', 'created_at', 'narx', 'tuladi', 'qoldi']


class TezTashxisSer(serializers.ModelSerializer):
    bemor = serializers.PrimaryKeyRelatedField(queryset=Bemor.objects.all())

    class Meta:
        model = Tashxis
        fields = ['id', 'bemor', 'date', 'diagnoz', 'tashxis', 'narx']

    def create(self, validated_data):
        bemor_data = validated_data.pop('bemor')
        bemor, created = Bemor.objects.get_or_create(**bemor_data)

        validated_data['bemor'] = bemor
        return super().create(validated_data)