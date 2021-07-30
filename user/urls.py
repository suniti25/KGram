from django.urls import path, re_path

from .views import image_upload, list, listOne, listUnfollowed, create, login, followUser, getFollows, refreshToken

urlpatterns = [
    path('', list, name="list users"),
    path('explore/', listUnfollowed, name="list unfollowed users"),
    path('create/', create, name="register user"),
    path('login/', login, name="check user login"),
    path('refreshtoken/', refreshToken, name="check user login"),
    path('follow/', followUser, name="follow another user login"),
    path('follow/list/', getFollows, name="list followings"),
    re_path(r'^upload/(?P<filename>[^/]+)$', image_upload),
    path('<int:id>/', listOne, name="list one user"),
]
