from django.shortcuts import render
from django.views import generic
from .models import Post, RepeatBlog
from django.utils import timezone
from django.http import HttpResponse
import datetime

class PostList(generic.ListView):
    queryset = Post.objects.filter(publish=True).order_by("-created_on").filter(created_on__lte=timezone.now(), created_on__gt=timezone.now()-datetime.timedelta(days=30))
    template_name = "feed.html"

class PostDetail(generic.DetailView):
    model = Post
    template_name = "post_detail.html"

class BlogNameList(generic.ListView):
    model = RepeatBlog
    template_name = "blog_archive.html"

class PostList(generic.ListView):
    queryset = Post.objects.filter(publish=True).order_by("-created_on")
    template_name = "repeat_blog_posts.html"

def RepeatBlogPosts(request, blogname):
    name_id = RepeatBlog.objects.get(name=blogname)
    queryset = Post.objects.filter(name=name_id).filter(publish=True).order_by("-created_on")
    context = {
        "post_list" : queryset
    }
    return render(request, "repeat_blog_posts.html", context)

def index(request):
    return render(request, "index.html")
