from django.urls import path
from .views import index, signup, signin, logout, settings, upload, like_post, profile, follow, search, delete, advanced, privacy, followers, following, add_comment, like_list, private, del_comment, posts

urlpatterns = [
    path('', index, name='index'),
    path('settings', settings, name='settings'),
    path('advanced-settings', advanced, name='advanced-settings'),
    path('privacy', privacy, name='privacy'),
    path('upload', upload, name='upload'),
    path('profiles/<str:pk>', profile, name='profile'),
    path('follow', follow, name='follow'),
    path('search', search, name='search'),
    path('followers/<str:pk>', followers, name='followers'),
    path('following/<str:pk>', following, name='following'),
    path('posts/<str:pk>', posts, name='posts'),
    path('likes/<uuid:post_id>', like_list, name='like_list'),
    path('like-post', like_post, name='like-post'),
    path('delete/<uuid:post_id>', delete, name='delete'),
    path('signup/', signup, name='signup'),
    path('signin/', signin, name='signin'),
    path('logout/', logout, name='logout'),
    path('post/<uuid:post_id>/comment/', add_comment, name='add_comment'),
    path('comment/delete/<int:comment_id>/',del_comment, name='del_comment'),
    path('private', private, name='private'),
]