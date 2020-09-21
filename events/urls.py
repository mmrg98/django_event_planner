from django.urls import path
from .views import (Login, Logout, Signup, home, EventsList,
 					EventDetail, UpdateEvent, CreateEvent)



urlpatterns = [

	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
	path('list/', EventsList.as_view(), name='list'),
	path('detail/<int:event_id>', EventDetail.as_view(), name='detail'),
	path('update/<int:event_id>', UpdateEvent.as_view(), name='update'),
	path('create/', CreateEvent.as_view(), name='create'),

]
