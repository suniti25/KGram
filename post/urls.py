from django.urls import path, re_path

from .views import comment_detail, create_comment, getFacebookPosts, getLikeCountByPost, getLikesByPost, image_upload, list, listOneById, listOneByUser, create, listOneByUserByEmail, list_comment, postLike, getFeed

urlpatterns = [
    path("", list, name="list posts"),
    path("byUser/email/<str:email>/", listOneByUserByEmail, name="list post by email of a user"),
    path("byUser/<int:user_id>/", listOneByUser, name="list post by user"),
    path("create/", create, name="make posts"),
    path("feed/", getFeed, name="list feed"),
    path("like/list/<int:post>/", getLikesByPost, name="list likes on a post"),
    path("like/<int:post>/", getLikeCountByPost, name="get count of likes on a post"),
    path("like/", postLike, name="like a post"),
    path("comment/create/", create_comment, name="create comment"),
    path("comment/count/<int:post>/", comment_detail, name="number of comments"),
    path("comment/lists/<int:post>/", list_comment, name="list of comments"),
    path("notices/", getFacebookPosts, name="facebook posts"),
    re_path(r'^upload/(?P<filename>[^/]+)$', image_upload),
    path("<int:id>/", listOneById, name="list one post"),
]
