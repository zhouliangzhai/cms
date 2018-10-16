from django.db import models

from tinymce.models import HTMLField

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="用户名称")
    password = models.CharField(max_length=50, verbose_name="用户密码")
    age = models.IntegerField(default=18, verbose_name="用户年龄")
    nickname = models.CharField(max_length=255, verbose_name="用户昵称")
    birthday = models.DateTimeField(auto_now_add=True)
    # header = models.CharField(max_length=255, default="/static/img/default.png", verbose_name="用户头像")
    header = models.ImageField(upload_to='static/img/headers/', default="static/img/default.png", verbose_name="用户头像")
    class Meta:
        ordering = ["id"]

    def __str__(self):
        return  self.name



class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name="文章标题")
    # content = models.TextField()
    content = HTMLField()
    publishTime = models.DateTimeField(auto_now_add=True)
    modifyTime = models.DateTimeField(auto_now=True)

    # 外键
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-publishTime']

    def __str__(self):
        return  self.title