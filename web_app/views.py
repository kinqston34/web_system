from typing import Any
from django.shortcuts import render,redirect,HttpResponse
from web_app.models import Visitor,Picture
from web_app.forms import LoginForm,RegiesterForm,PictureForm,ResetPasswordForm
from django.urls import reverse
from django.views.generic import TemplateView,ListView
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from web_app.crawls.ithome_news import IThome_News,IThome_Tech,IThome_Security
from web_app.crawls.technews import TechNews,TechNews_Net,TechNews_Tech,TechNews_Semi
from random import randint 

# Create your views here.

class Homelist(ListView): 
    model = Visitor
    template_name = "home_list.html"
    context_object_name = "db_list"

    def get_context_data(self,**kwargs):     #overwriting get_context_data --> **kwargs = {}
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session["login_user"]
        return context

class IndexCardView(TemplateView):
    template_name = "index_navbar.html"

    def get_context_data(self, **kwargs):
        content = super().get_context_data(**kwargs)
        url = self.request.get_full_path_info()    #得到index/<> 網址web_app後半段
        if "IThome" in url:
            if "product" in url:
                news = IThome_Tech()
            elif "security" in url:
                news = IThome_Security()
            else:
                news = IThome_News()
        elif "TechNews" in url:
            if "tech" in url:
                news = TechNews_Tech()
            elif "semi" in url:
                news = TechNews_Semi()
            elif "net" in url:
                news = TechNews_Net()
            else:
                news = TechNews()
        content["data"] = news.news_django_used()
        content["newsname"] = news.__str__
        return content
#==============  function =================#
def test(request,type=None):
    return render(request,"forget_password2.html",{"token":True,"user":"aaa"})

def index_card(request):
    request.get_full_path_info()
    return render(request,"index.html")

def login(request,login=None):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():     #確認表單有無合法輸入
            user = form.cleaned_data["user"]
            password = form.cleaned_data["password"]
            print("帳號",user)
            print("密碼",password)
            if user and password:    #確認帳號密碼 是否都是對的
                request.session['login_user'] = user
                responese = redirect('home')
                responese.set_cookie("login_id","1")
                return responese
            else:
                return render(request,"login.html",{"login":"error"})
        else:
            return render(request,"login.html",{"login":"elligal"})
    else:
        if 'login_id' in request.COOKIES :
            return redirect('home')
        if 'modify_password' in request.COOKIES and request.COOKIES['modify_password'] == "success":
            responese = render(request,"login.html",{"modify":"success"})
            responese.delete_cookie("modify_password")
            return responese
        return render(request,"login.html")

def logout(request):

    if 'login_user' in request.session :
        # user = request.COOKIES['user']
        # print(user)
        user = request.session['login_user']
        del request.session['login_user']
        res = render(request,"login.html",{"user":user,"login":"False"})
        res.delete_cookie('login_id')
        return res
    else:
        return redirect("index")
#============== 忘記密碼 =================#
def forget_password(request,rand=None):
    
    if request.method == "POST":
        user = request.POST["user"]
        data = db_visitor_read(user=user)
        if data == False:
            username = False
        else:
            #寄發修改密碼帳戶確認驗證信
            username = [True,data.user]
            send_forget_email(request,data.user)    #傳送email
            # print(request.session['rand'])
        return render(request,"forget_password2.html",{"user":username}) 
    
    if request.session['rand'] == rand:   #驗證信成功   
        user = request.session["user"]
        return render(request,"forget_password2.html",{"token":True,"user":user})
    else:
        if rand == None:
            return render(request,"forget_password2.html")
        else:                
            return render(request,"forget_password2.html",{"token":False})
    
def reset_password(request):
    
    if request.method == "POST":
        user = request.session["user"]
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            again = form.cleaned_data['again']
            if password != again :
                return render(request,"forget_password2.html",{"token":True,"user":user,"error":True})
            else:
                data = Visitor.objects.get(user=user)
                data.password = password
                data.save()
                respone = redirect("login")
                respone.set_cookie("modify_password","success")
                return respone
        else:
            return render(request,"forget_password2.html",{"token":True,"user":user,"error":"more"})

def send_forget_email(request,user=None):
    
    def sendemail():
        rand = str(randint(1,10000))
        request.session["rand"] = rand
        email_template = render_to_string(
            "forget_email.html",
            {"user":user,"rand":rand},
        )
        email = EmailMessage(
            '修改密碼通知信',  #email title
            email_template,   #email content
            "aa3741867@gmail.com", #寄件者
            ["aa37741867@gmail.com"], #收件者
        )
        email.content_subtype = "html" #content 轉換成html格式
        email.send()

    if user !=None:
        request.session["user"] = user
        sendemail()
    elif request.session["user"] != None:
        user = request.session["user"]
        sendemail()
        return render(request,"forget_password2.html",{"user":[True,user]})
#==============  home 後台 =================#    
def home(request):

    if request.COOKIES['login_id'] == "1":
        user = request.session["login_user"]
        return render(request,"home.html",{"username":user})
    else:
        return redirect("login")

#==============  註冊 =================#
def register(request,register=None):

    if request.method == "POST":
        form  = RegiesterForm(request.POST)
        if form.is_valid():

            user = form.cleaned_data["user"]
            password = form.cleaned_data["password"]
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            print("user : ",user)
            print("password : ",password)
            print("name : ",name)
            print("email : ",email)
            if user :
                db_visitor_insert(user,password,name,email)
                print("資料庫儲存成功")
                responese = redirect('register_success')
                responese.set_cookie("register",user)
                return responese
            return render(request,"register.html",{"register":"registered"})
        else:
            return render(request,"register.html",{"register":"error"})
    else:
        return render(request,"register.html")

def register_success(request):

    if "register" in request.COOKIES:
        user = request.COOKIES['register']
        read = Visitor.objects.get(user = user)
        title = "親愛的,"+read.name+"您好，這是網站驗證信"
        content = render_to_string("vertified_email.html",{"username":read.name},request)
        sender = "aa3741867@gmail.com"
        email_res = send_mail(title,"",sender,["aa37741867@gmail.com"],html_message=content)
        #===註冊驗證===#
        return render(request,"login.html",{"login":"register"})
    else:
        return HttpResponse("404")
#==============  照片上傳 =================#
def pictureupdate(request):
    saved = 1
    if request.method == "POST":
        pictureform = PictureForm(request.POST,request.FILES)
        if pictureform.is_valid():
            picture = Picture()
            picture.filename = pictureform.cleaned_data['filename']
            picture.picture = pictureform.cleaned_data['picture']
            picture.save()
            saved = True
        else:
            saved = False

    return render(request,"picture.html",{"save":saved})

#============== 資料庫 Visitor crud =================#
def db_visitor_insert(user,password,name,email): #Visitor 新增資料

    visitor = Visitor()
    visitor.user = user
    visitor.password = password
    visitor.name = name
    visitor.email = email
    visitor.save()

def db_visitor_read(user=None):  #Visitor 讀取資料

    if user != None:
        try:
            read = Visitor.objects.get(user = user)
        except:
            return False
            # return HttpResponse("您指定的帳號查無資料")
    else:
        read = Visitor.objects.all()
    return read

def db_visitor_delete(user):  ##Visitor 刪除資料

    try:
        read = Visitor.objects.get(user = user)
    except:
        return HttpResponse("沒有此帳戶,刪除失敗")
    else:
        read.delete()

def db_visitor_update(user,password,name,email):  #Visitor 修改資料

    try:
        read = Visitor.objects.get(user = user)
    except:
        return HttpResponse("沒有此帳戶，新增失敗")
    else:
        db_visitor_delete(user)
        db_visitor_insert(user,password,name,email)










