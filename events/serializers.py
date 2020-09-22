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
'''
from rest_framework.views import APIView
from rest_framework.generics import (
	ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
	)
from .serializers import (CreatEventSerializer, EventsSerializer,
	EventDetailSerializer
	)

from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

class EventsList(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'event_list.html'

	def get(self, request):
		queryset = Events.objects.filter(datetime__gte=datetime.today())
		query = request.GET.get("q")
		if query:
			queryset = queryset.filter(
			Q(title__icontains=query)|
			Q(user__username__icontains=query)|
			Q(description__icontains=query)
			).distinct()
		return Response({'events': queryset})


class EventDetail(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'event_detail.html'

	def get(self, request,event_id):
		queryset = Events.objects.get(id=event_id)
		return Response({'event': queryset})


class CreateEvent(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'event_create.html'

	def get(self, request):
		serializer = CreatEventSerializer()
		return Response({'serializer': serializer})

	def post(self, request):
		serializer = CreatEventSerializer(data=request.data)
		if not serializer.is_valid():
			return Response({'serializer': serializer, 'event': event})

		serializer.save(user=self.request.user)
		return redirect('list')


class UpdateEvent(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'event_update.html'

	def get(self, request, event_id):
		event = get_object_or_404(Events, id=event_id)
		serializer = CreatEventSerializer(event)
		return Response({'serializer': serializer, 'event': event})

	def post(self, request, event_id):
		event = get_object_or_404(Events, id=event_id)
		serializer = CreatEventSerializer(event, data=request.data)
		if not serializer.is_valid():
			return Response({'serializer': serializer, 'event': event})

		serializer.save()
		return redirect('list')


class EventDelete(DestroyAPIView):
	queryset = Events.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
'''
