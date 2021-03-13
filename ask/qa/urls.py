from django.conf.urls import url
from qa.views import question_details

urlpatterns = [
    url(r'^(?P<id>\d+)/$', question_details),
    ]
