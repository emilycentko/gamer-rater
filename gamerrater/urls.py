from rest_framework import routers
from django.conf.urls import include
from django.urls import path
from gamerraterapi.views import GameView, CategoryView
from gamerraterapi.views import register_user, login_user

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'games', GameView, 'game')
router.register(r'categories', CategoryView, 'game')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
]
