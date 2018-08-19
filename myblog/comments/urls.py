from django.conf.urls import url
from .views import (
    post_comment,
    CommentCreateView,
)

app_name = 'comments'

urlpatterns = [
    # url(r'^post_comment/(?P<pk>\d+)/$', post_comment, name='post_comment'),
    url(r'^post_comment/(?P<pk>\d+)/$', CommentCreateView.as_view(), name='post_comment'),
]