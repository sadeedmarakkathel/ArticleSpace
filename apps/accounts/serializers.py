from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_role(self, value):
        if value == User.ADMIN:
            raise serializers.ValidationError("Cannot register as an Admin.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
