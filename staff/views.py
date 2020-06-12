from django.shortcuts import render
from blog.models import Post
from django.views import generic
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models
from django.contrib.auth.models import User
from users.models import staff_check, editor_check, author_check

class CreatePost(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ["title", "content", "name", "status"]
    template_name = "staff/post_create.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def test_func(self):
        get_test_func(author_check)

class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ["title", "content", "name", "status"]
    template_name = "staff/post_author_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class EditorUpdatePost(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ["title", "content", "name", "publish"]
    template_name = "staff/post_editor_update.html"

    def form_valid(self, form):
        form.instance.slug = slugify(form.instance.title)
        return super().form_valid(form)

    def test_func(self):
        get_test_func(editor_check)

class DeletePost(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = "{% url 'home' %}"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@user_passes_test(editor_check, login_url="{% url 'home' %}")
@login_required
def editorPostList(request):
    queryset = Post.objects.filter(publish=False).order_by("created_on")
    context = {
        "post_list" : queryset
    }
    return render(request, "staff/author_posts.html", context)

@user_passes_test(author_check, login_url="{% url 'home' %}")
@login_required
def authorPostList(request, authorname):
    author_idnumber = User.objects.get(username=authorname)
    queryset = Post.objects.filter(author=author_idnumber).filter(status=1).order_by("-created_on")
    context = {
        "post_list" : queryset
    }
    return render(request, "staff/author_posts.html", context)

@user_passes_test(staff_check, login_url="{% url 'home' %}")
@login_required
def staffProfilePage(request):
    return render(request, "staff/staff_profile.html")

def unauthorisedPage(request):
    return render(request, "staff/unauthorisedpage.html")

@user_passes_test(staff_check)
@login_required
def staffHomePage(request):
    return render(request, "staff/staffhomepage.html")
