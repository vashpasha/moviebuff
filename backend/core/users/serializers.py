from rest_framework import serializers
from .models import UserData
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserData
        fields = ["id", "email", "name", "password"]

    def create(self, validated_data):
        user = UserData.objects.create(email=validated_data['email'],
                                       name=validated_data['name']
                                         )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['id', 'email', 'name', 'bio', 'date_joined', 'is_active', 'is_admin']

class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserData
        fields = ['name', 'bio', 'email']

        def update(self, instance, validated_data):
            instance.name = validated_data.get('name', instance.name)
            instance.bio = validated_data.get('bio', instance.bio)
            instance.email = validated_data.get('email', instance.email)
            instance.save()
            return instance

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_new_password = serializers.CharField(required=True)

    def validate(self, data):
        user = self.context['request'].user
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        confirm_new_password = data.get('confirm_new_password')

        if not user.check_password(current_password):
            raise serializers.ValidationError({"current_password": "Current password is incorrect."})

        if new_password != confirm_new_password:
            raise serializers.ValidationError({"confirm_new_password": "New password fields didn't match."})

        return data

    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance