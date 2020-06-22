from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views
from blog.views import index
from .forms import ProfileUpdateForm

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect(index)
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})

@login_required
def UserProfilePage(request):
    return render(request, "users/user_profile_page.html")

@login_required
def UserProfilePageUpdate(request):
    if request.method == "POST":
        user_form = ProfileUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f"Your account has been updated!")
            return redirect('profilePage')
    else:
        user_form = ProfileUpdateForm(instance=request.user)

    context = {
        'user_form': user_form
    }
    return render(request, "users/user_profile_update.html", context)
