from django.contrib import admin
from .models import Post, RepeatBlog
from staff.models import StaffMember

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','created_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user')

admin.site.register(Post, PostAdmin)
admin.site.register(RepeatBlog)
admin.site.register(StaffMember, StaffMemberAdmin)
