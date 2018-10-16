from io import BytesIO
import uuid
import logging

from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.shortcuts import render, redirect, reverse
# from django.core.urlresolvers import reverse
from django.core.cache import cache
from django.views.decorators.http import require_GET,require_http_methods,require_POST,require_safe
from django.forms.models import model_to_dict
from django.core.serializers import  serialize
from django.conf import settings
from django.core.paginator import Paginator


from . import models
from . import utils
from . import cacheUtils

def index(request):
    logger = logging.getLogger("django")
    logger.debug("首页开始运行了")
    pageSize = int(request.GET.get("pageSize",settings.PAGE_SIZE))
    pageNow = int(request.GET.get("pageNow",1))
    articles = cacheUtils.getAllArticle()
    #使用django自带的分页器，首先构建一个paginator对象
    paginator = Paginator(articles,pageSize)
    page = paginator.page(pageNow)
    # return render(request, "blog/index.html", {"articles": articles})
    return render(request, "blog/index.html", {"page": page, "pageSize": pageSize})


def add_user(request):
    return render(request, "blog/add_user.html", {})


def delete_user(request, user_id):
    # u_id = request.GET["id"]
    user = models.User.objects.get(pk=user_id)
    user.delete()
    # users = models.User.objects.all()
    # return render(request, "blog/user_list.html", {"msg": "删除用户成功！！", "users": users})
    # return HttpResponseRedirect("/blog/list_user/")
    # return redirect("/blog/list_user/")
    return redirect(reverse("blog:list_user"))

@utils.require_login
def list_user(request):
    users = models.User.objects.all()
    return render(request, "blog/user_list.html", {"users": users})


def reg(request):
    if request.method == "GET":
        return render(request, "blog/add_user.html", {"msg": "请认真填写如下选项"})
    elif request.method == "POST":
        # 接受参数
        try:
            username = request.POST["username"].strip()
            password = request.POST.get("password").strip()  # .getlist()
            confirmpwd = request.POST.get("confirmpwd").strip()
            nickname = request.POST.get("nickname", None)

            avatar = request.FILES.get("avatar",None)
            # code = request.POST['code']
            #
            #
            # mycode = request.session['code']
            # if code.upper() != mycode.upper():
            #     return render(request, "blog/add_user.html", {"msg": "验证码输入有误！！"})
            #
            # #删除session验证码‘
            # del request.session['code']
            # 数据校验
            if len(username) < 1:
                return render(request, "blog/add_user.html", {"msg": "用户名称不能为空！！"})
            if len(password) < 6:
                return render(request, "blog/add_user.html", {"msg": "密码长度不能小于6位！！"})
            if password != confirmpwd:
                return render(request, "blog/add_user.html", {"msg": "两次密码不一致！！"})
            # 用户名称是否重复
            try:
                user = models.User.objects.get(name=username)
                return render(request, "blog/add_user.html", {"msg": "该用户名称已经存在，请重新填写！！"})
            except:
                #先对密码加密，之后在保存
                password = utils.hmac_by_md5(password)

                user = models.User(name=username, password=password, nickname=nickname, header=avatar)
                user.save()
                return render(request, "blog/add_user.html", {"msg": "恭喜您，注册成功！！"})

                # 保存数据
                # try:
                # avatar = request.FILES['avatar']
                # 保存图片
                # path = "static/img/headers/" + uuid.uuid4().hex + avatar.name
                # with open(path, "wb") as f:
                #     for file in avatar.chunks():
                #         f.write(file)

                # user = models.User(name=username, password=password, nickname=nickname, header=avatar)
                #     user.save()
                #     return render(request, "blog/add_user.html", {"msg": "恭喜您，注册成功！！"})
                # except Exception as e:
                #     print(e)
                #     user = models.User(name=username, password=password, nickname=nickname)
                #     user.save()
                #     return render(request, "blog/add_user.html", {"msg": "恭喜您，注册成功！！"})
        except:
            return render(request, "blog/add_user.html", {"msg": "对不起，用户名称不能为空！！"})

@utils.require_login
def show(request, u_id):
    user = models.User.objects.get(pk=u_id)
    return render(request, "blog/show.html", {"user": user})


def update(request, u_id):
    if request.method == "GET":
        user = models.User.objects.filter(id=u_id).first()
        return render(request, "blog/update.html", {"user": user})
    else:
        nickname = request.POST["nickname"]
        age = request.POST['age']

        # 数据校验

        # 如何修改？？？？？？？？？？
        # 第一步，获取用户
        user = models.User.objects.get(pk=u_id)
        # 第二步，修改值
        user.age = age
        user.nickname = nickname
        # 第三步， 保存
        user.save()

        # return redirect("/blog/show/" + str(u_id) + "/")
        return redirect(reverse("blog:show", args=(u_id,)))


def login(request):
    """
    登录的视图函数，完成用户登录功能
    :param request: 请求头对象
    :return:
    """
    if request.method == "GET":
        return render(request, "blog/login.html", {"msg": "请登录"})
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        # TODO 将来需要完善验证码
        code = request.POST['code']
        checkbox = request.POST['checkbox']
        print(checkbox)

        mycode = request.session['code']
        if code.upper() != mycode.upper():
            return render(request, "blog/login.html", {"msg": "验证码输入有误！！"})

        # 删除session验证码‘
        del request.session['code']

        try:
            password = utils.hmac_by_md5(password)
            user = models.User.objects.get(name=username, password=password)
            # 使用session来记录登录用户的信息
            request.session["loginUser"] = user
            # 使用cookie记住用户名称
            response = redirect(reverse("blog:index"))
            if (checkbox):
                #cookie不能存储中文
                response.set_cookie("username",user.name,expires=3600*24*14)
                # return redirect(reverse("blog:index"))
                return response
        except:
            return  render(request, "blog/login.html", {"msg": "登录失败，请重新登录！！"})



def logout(req):
    try:
        del req.session["loginUser"]
    finally:
        return redirect(reverse("blog:index"))

@utils.require_login
def add_article(request):
    if request.method == "GET":
        return render(request, "blog/add_article.html", {"msg": "请认真填写如下选项"})
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        author = request.session["loginUser"]

        # 验证
        article = models.Article(title=title, content=content, author=author)
        article.save()

        #将缓存重新更新
        cacheUtils.getAllArticle(ischanage=True)
        cacheUtils.getSELFArticle(author=author,ischanage=True)
        # return redirect(reverse("blog:show_arcticle", kwargs={"a_id": article.id }))
        return JsonResponse({"msg":"文章添加成功","success":True})

def delete_article(request, a_id):
    at = models.Article.objects.get(pk=a_id)
    at.delete()
    cacheUtils.getAllArticle(ischanage=True)
    return redirect(reverse("blog:index"))



def update_article(request, a_id):
    at = models.Article.objects.get(pk=a_id)
    if request.method == "GET":
        return render(request, "blog/update_article.html", {"article":at})
    else:
        try:
            title = request.POST["title"]
            content = request.POST["content"]
            at.title = title
            at.content = content
            at.save()
            return redirect(reverse("blog:show_arcticle", kwargs={"a_id": a_id}))
            # return render(request, "blog/index.html", {"a_id":a_id})

        except Exception as e:
            print(e)
            return render(request, "blog/show_at.html", {"article": at})

def show_arcticle(request, a_id):
    at = models.Article.objects.get(pk=a_id)
    return render(request, "blog/show_at.html", {"article": at})

@utils.require_login
def self_article(request):
    autho = request.session["loginUser"]
    print(autho)

    return render(request, "blog/self_article.html",{})

def code(request):
    img,code = utils.create_code()
    #首先需要将code保存到session中
    request.session['code']=code

    #返回图片
    file = BytesIO()
    img.save(file,'PNG')
    return HttpResponse(file.getvalue(),"image/png")


def checkusername(request,username):
   qs = models.User.objects.filter(name=username)
   if len(qs) > 0:
       return JsonResponse({
           "msg":"该用户名已经存在，请重新输入！！","success":False
       })
   else:
       return JsonResponse({
           "msg":"恭喜您，用户名可以适应","success":True
       })
