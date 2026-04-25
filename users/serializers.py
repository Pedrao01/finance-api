from rest_framework import serializers
from .models import User, Transaction


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'cpf', 'phone_number', 'password']


class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'value', 'kind', 'status', 'created_at', 'user']
