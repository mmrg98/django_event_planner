from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import UserSignup, UserLogin, EventForm, BookForm
from django.contrib.auth.models import User
from .models import Events, Book
from django.contrib import messages

from datetime import datetime
from django.db.models import Q
#from .permissions import IsOwner, EditTask, EditBoard


def home(request):
    events = Events.objects.filter(user=request.user)
    context={"events": events}
    return render(request, 'home.html',context)

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
                return redirect('home')
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")


############################################################################ event Events
def event_list(request):
    events = Events.objects.filter(datetime__gte=datetime.today())
    if request.user.is_staff:
        events = Events.objects.all()
    query = request.GET.get("q")
    if query:
        events = events.filter(
        Q(title__icontains=query)|
        Q(user__username__icontains=query)|
        Q(description__icontains=query)
        ).distinct()
    context = {
        "events": events,
    }
    return render(request, 'event_list.html', context)


def event_detail(request, event_id):
    event=Events.objects.get(id=event_id)
    context = {
        "event": event,
    }
    return render(request, 'event_detail.html', context)

'''def user_profile(request, user_id):
    u= User.objects.get(id=user_id)
    hiss = Log.objects.all()
    context = {
        "hiss":hiss,
}
    return render(request, 'user_profile.html',context)
'''
def event_create(request):
    if request.user.is_anonymous:
        return redirect('signin')
    if not request.user.is_staff:
        return redirect('list')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.user = request.user
            event.save()
            return redirect('list')
    context = {
        "form":form,
    }
    return render(request, 'event_create.html', context)

def event_update(request, event_id):
    if request.user.is_anonymous:
        return redirect('signin')
    if not request.user.is_staff:
        return redirect('list')
    event = Events.objects.get(id=event_id)
    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():

            form.save()
            return redirect('list')
    context = {
        "event": event,
        "form":form,
    }
    return render(request, 'event_update.html', context)

def event_delete(request, event_id):
    if request.user.is_anonymous:
        return redirect('signin')
    if not request.user.is_staff:
        return redirect('list')
    event = Events.objects.get(id=event_id)
    event.delete()
    return redirect('list')

def book_event(request, event_id):
    form = BookForm()
    event = Events.objects.get(id=event_id)
    if request.user.is_anonymous:
        return redirect('signin')
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.event = event
            book.guest= request.user
            book.save()
            return redirect('detail', event_id)
    context = {
        "form":form,
        "event": event,
    }
    return render(request, 'book.html', context)


'''
    event = Events.objects.get(id=event_id)
    form = BookForm()
    if request.user.is_anonymous:
        return redirect('signin')
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.event= event
            book.user = request.user
            book.event.seats -=1
            event.save()
            messages.success(request, "You have successfully booked.")
            return redirect('list')
    context = {
        "form":form,
    }
    return render(request, 'book.html', context)
'''
