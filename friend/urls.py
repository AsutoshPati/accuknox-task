from django.urls import path
from .views import *

urlpatterns = [
    path('find-friends', list_users),
    path('friend', FriendView.as_view()),
]
