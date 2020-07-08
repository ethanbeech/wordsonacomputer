from django.contrib import admin
from .models import Post, RepeatBlog, Comment
from staff.models import StaffMember

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status','updated_on')
    list_filter = ("status",)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}

class RepeatBlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user')

class CommentAdmin(admin.ModelAdmin):
    list_display = ("author", "post", "created_on", "censored")
    list_filter = ("post",)

admin.site.register(Post, PostAdmin)
admin.site.register(RepeatBlog, RepeatBlogAdmin)
admin.site.register(StaffMember, StaffMemberAdmin)
admin.site.register(Comment, CommentAdmin)
