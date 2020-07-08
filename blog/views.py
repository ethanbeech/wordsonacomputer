from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
from django.views import generic
from .models import Post, RepeatBlog
from staff.models import StaffMember
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
import datetime

class PostList(generic.ListView):
    queryset = Post.objects.filter(publish=True).order_by("-updated_on").filter(updated_on__lte=timezone.now(), created_on__gt=timezone.now()-datetime.timedelta(days=180))
    template_name = "feed.html"

class BlogNameList(generic.ListView):
    model = RepeatBlog
    template_name = "blog_archive.html"

class PostList(generic.ListView):
    queryset = Post.objects.filter(publish=True).order_by("-updated_on")
    template_name = "repeat_blog_posts.html"

class AboutList(generic.ListView):
    model = StaffMember
    template_name = "about.html"

def PostDetail(request, slug):
    template_name = "post_detail.html"
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.all()
    new_comment = None
    # Creating new comment
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user
            new_comment.censored = False
            # Save the comment to the database
            new_comment.save()
            # Reset comment form so it is now blank
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def RepeatBlogPosts(request, blogname):
    name_id = RepeatBlog.objects.get(name=blogname)
    queryset = Post.objects.filter(name=name_id).filter(publish=True).order_by("-updated_on")
    context = {
        "post_list" : queryset
    }
    return render(request, "repeat_blog_posts.html", context)

def index(request):
    return render(request, "index.html")
