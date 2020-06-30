from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from blog.models import Post
from .models import StaffMember
from django.views import generic
from django.utils.text import slugify
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import models
from users.models import staff_check, editor_check, author_check
from .forms import StaffUpdateForm
from users.forms import ProfileUpdateForm


class CreatePost(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ["title", "content", "name", "status"]
    template_name = "staff/post_create.html"
    success_url = reverse_lazy("staff_home")

    def form_valid(self, form):
        current_user_id = self.request.user.id
        staff_profile = StaffMember.objects.get(user=current_user_id)
        form.instance.author = self.request.user
        form.instance.author_name = staff_profile
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
    return render(request, "staff/editor_posts.html", context)

@user_passes_test(author_check, login_url="{% url 'home' %}")
@login_required
def authorPostList(request, authorname):
    author_idnumber = User.objects.get(username=authorname)
    queryset = Post.objects.filter(author=author_idnumber).filter(status=1).order_by("-created_on")
    context = {
        "post_list" : queryset
    }
    return render(request, "staff/author_posts.html", context)

@user_passes_test(staff_check)
@login_required
def staffProfilePage(request):
    current_user_id = request.user.id
    staff_profile = StaffMember.objects.get(user=current_user_id)
    user_profile = User
    context = {
        'staff_profile': staff_profile,
    }
    return render(request, "staff/staff_profile.html", context)

@user_passes_test(staff_check, login_url="{% url 'home' %}")
@login_required
def staffProfilePageUpdate(request):
    current_user_id = request.user.id
    if request.method == "POST":
        staff_form = StaffUpdateForm(request.POST, request.FILES, instance=StaffMember.objects.get(user=current_user_id))
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        if staff_form.is_valid() and user_form.is_valid():
            staff_form.save()
            user_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect('staff_profile_page')
    else:
        staff_form = StaffUpdateForm(instance=StaffMember.objects.get(user=current_user_id))
        user_form = ProfileUpdateForm(instance=request.user)

    context = {
        'staff_form': staff_form,
        'user_form': user_form
    }
    return render(request, "staff/staff_profile_update.html", context)

def unauthorisedPage(request):
    return render(request, "staff/unauthorisedpage.html")

@user_passes_test(staff_check)
@login_required
def staffHomePage(request):
    return render(request, "staff/staffhomepage.html")
