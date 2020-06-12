from django.db import models
from django.contrib.auth.models import User

def staff_check(user):
    if user.groups.filter(name = "staff").exists():
        return True
    if user.groups.filter(name = "admin").exists():
        return True

def editor_check(user):
    if user.groups.filter(name = "editor").exists():
        return True
    if user.groups.filter(name = "admin").exists():
        return True

def author_check(user):
    if user.groups.filter(name = "author").exists():
        return True
    if user.groups.filter(name = "admin").exists():
        return True
