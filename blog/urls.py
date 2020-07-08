from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="home"),
    path("blogarchive/", views.BlogNameList.as_view(), name="blogArchive"),
    path("feed/", views.PostList.as_view(), name="feed"),
    path("about/", views.AboutList.as_view(), name="about"),
    path("repeatblogposts/<blogname>/", views.RepeatBlogPosts, name="repeat_blog_posts"),
    path("<slug:slug>/", views.PostDetail, name="post_detail"),
]
