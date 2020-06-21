from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class StaffMember(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=800, blank=True)
    profile_picture = models.ImageField(default='profile_pics/defaultProfilePicture.png', upload_to="profile_pics")
    full_name = models.CharField(max_length=100, default="unspecified", blank=True)

    def __str__(self):
        return self.description

    def save(self):
        super().save()

        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)
