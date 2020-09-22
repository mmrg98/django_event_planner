from django.urls import path
from .views import *
from events import views



urlpatterns = [

	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
	path('list/', views.event_list, name='list'),
	path('detail/<int:event_id>', views.event_detail, name='detail'),
	path('create/', views.event_create, name='create'),
    path('update/<int:event_id>',views.event_update, name='update'),
    path('delete/<int:event_id>', views.event_delete, name='delete'),
	path('book/<int:event_id>',views.book_event, name='book'),
	path('profile/<int:user_id>/',views.user_profile  ,name='profile'),

]
