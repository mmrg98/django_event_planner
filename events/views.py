from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin
from django.contrib.auth.models import User
from .models import Events

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
#from .permissions import IsOwner, EditTask, EditBoard


def home(request):
    return render(request, 'home.html')

class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")


############################################################################
#class Register(CreateAPIView):
#    serializer_class = RegisterSerializer

class EventCreate(CreateAPIView):
    serializer_class = CreatEventSerializer
    permission_classes = [IsAuthenticated]
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class EventsList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'event_list.html'

    def get(self, request):
        queryset = Events.objects.all()
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
		return Response({'serializer': serializer})


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
	lookup_url_kwarg = 'board_id'
