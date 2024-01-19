from django.urls import re_path as url
from web_app import views
from django.views.generic import TemplateView,ListView
from web_app.models import Visitor
from web_app.views import IndexCardView

urlpatterns = [
    # TemplateView.as_view (extra_context={'login': "illegal"})
    # url(r"^index/",views.index,name="index"),
    url(r"^test",views.test,name="test"),
    url(r"^index/$",TemplateView.as_view(template_name="index.html"),name="index"),
    url(r"^index/IThome/(?P<type>\w+)?",IndexCardView.as_view(),name= "IThome"),
    url(r"^index/TechNews/(?P<type>\w+)?",IndexCardView.as_view(),name= "TechNews"),
    url(r"^login/$",views.login,name="login"),
    url(r"^login/?$",views.register_success,name="register_success"),
    url(r"^login/forget_password/",views.forget_password,name="forget_password"),
    url(r"^login/forget_mail_vertified/(\d+)/",views.forget_email_vertified,name="forget_email_vertified"),
    url(r"^login/forget_email/*",views.send_forget_email,name="forget_email"),
    url(r"^logout/",views.logout,name="logout"),
    url(r"^home/",views.home,name="home"),
    url(r"^home_list/",views.Homelist.as_view(),name="home_list"),
    # url(r"^register/(?P<register>)*",views.register,name="register"),
    url(r"^register/",views.register,name="register"),
    url(r"^picture/",views.pictureupdate,name="pictureupdate"),


]


