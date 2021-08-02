from django.urls import path, re_path

from .views import getProfile, image_upload, list, listOne, listUnfollowed, create, login, followUser, getFollows, refreshToken, verifyEmail, resendVerificationCode

urlpatterns = [
    path('', list, name="list users"),
    path('explore/', listUnfollowed, name="list unfollowed users"),
    path('create/', create, name="register user"),
    path('login/', login, name="check user login"),
    path('refreshtoken/', refreshToken, name="check user login"),
    path('follow/', followUser, name="follow another user login"),
    path('follow/list/', getFollows, name="list followings"),
    path('profile/', getProfile, name="get user profile"),
    path('verify/', verifyEmail, name="verify user email"),
    path('resendVerification/', resendVerificationCode,
         name="resend verify email code"),
    re_path(r'^upload/(?P<filename>[^/]+)$', image_upload),
    path('<int:id>/', listOne, name="list one user"),
]
