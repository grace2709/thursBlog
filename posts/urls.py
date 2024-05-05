from django.urls import path
from .import views
app_name="posts"
from .feeds import LatestPostsFeed

urlpatterns=[
    #path("",views.home,name="home"),
    # path("",views.PostListView.as_view() ,name="posts"),posts
path("<int:year>/<int:month>/<int:day>/<slug:post>",views.post_detail,name="post_detail"),
    path("<int:post_id>/share/",views.post_share,name="post_share"),
    path("<int:id>/comment/",views.post_comment,name="comment"),
    path("tag/<slug:tag_slug>/",views.post_list,name="post_list_by_tag"),
    path("",views.post_list,name="post_list"),
    path("feed/",LatestPostsFeed(),name="post_feed"),
]