from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Events


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password']

	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		new_user = User(username=username)
		new_user.set_password(password)
		new_user.save()
		return validated_data


class CreatEventSerializer(serializers.ModelSerializer):
	class Meta:
		model = Events
		exclude = ['user',]


class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Events
        fields = ['title', 'location','datetime' ]


class EventDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Events
		fields = '__all__'
