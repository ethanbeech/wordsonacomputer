from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from staff.models import StaffMember

STATUS = (
    (0,"Draft"),
    (1,"Complete"),
)

class RepeatBlog(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_post")
    author_name = models.ForeignKey(StaffMember, on_delete=models.CASCADE, related_name="blog_post")
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS)
    publish = models.BooleanField(default=False)
    name = models.ForeignKey(RepeatBlog, on_delete=models.CASCADE, default="0")

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')

# Permissions
