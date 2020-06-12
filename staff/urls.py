from . import views
from django.urls import path

urlpatterns = [
    path("staffprofile/", views.staffProfilePage, name="staffprofile"),
    path("createpost/", views.CreatePost.as_view(), name="create_post"),
    path("unauthorisedpage/", views.unauthorisedPage, name="unauthorised_page"),
    path("staffhomepage/", views.staffHomePage, name="staff_home"),
    path("authorposts/<authorname>/", views.authorPostList, name="author_posts"),
    path("editorposts/", views.editorPostList, name="editor_posts"),
    path("<slug:slug>/update", views.UpdatePost.as_view(), name="update_post"),
    path("<slug:slug>/delete", views.DeletePost.as_view(), name="delete_post"),
    path("<slug:slug>/editorupdate", views.EditorUpdatePost.as_view(), name="editor_update_post")
]
