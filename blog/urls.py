from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="home"),
    path("blogarchive/", views.BlogNameList.as_view(), name="blogArchive"),
    path("feed/", views.PostList.as_view(), name="feed"),
    path("<slug:slug>/", views.PostDetail.as_view(), name="post_detail"),
    path("repeatblogposts/<blogname>/", views.RepeatBlogPosts, name="repeat_blog_posts")
]
