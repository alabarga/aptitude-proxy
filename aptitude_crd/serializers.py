from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Cuestionario, Componente


class UserSerializer(serializers.ModelSerializer):
    cuestionarios = Cuestionario.objects.all()
    # cuestionarios = serializers.PrimaryKeyRelatedField(many=True, queryset=Cuestionario.objects.all())
    class Meta:
        model = User
        fields = ('id', 'username', 'cuestionarios')


class CuestionarioSerializer(serializers.ModelSerializer):
    owner = User.objects.get(id=1)
    class Meta:
        model = Cuestionario
        fields = ('nombre', 'descripcion', 'owner')


class ComponenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Componente
        fields = '__all__'