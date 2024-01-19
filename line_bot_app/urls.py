from django.urls import re_path as url
from line_bot_app import views

urlpatterns = [
    url(r"^line/",views.line_test,name="line_test"),
    url(r"callback/",views.callback,name="callback"),
]

