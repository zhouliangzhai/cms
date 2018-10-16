from django.core.cache import  cache
from . import models


def getAllArticle(ischanage=False):
    """
    缓存查询首页所有文章
    :return:
    """
    print("开始加载首页数据")
    articles = cache.get("allArticle")
    if articles is None or ischanage:
        print("缓存中没有数据，开始查询数据库……")
        articles = models.Article.objects.all()
        print("数据库中查询到数据，同步到缓存中")
        cache.set("allArticle", articles)
    else:
        print("缓存中有数据……，不再查询数据库")

    return articles



def getSELFArticle(author,ischanage=False):
    """
    缓存查询个人文章
    :return:
    """
    print("开始加载个人文章数据")
    sfarticle = cache.get("self_article")
    if sfarticle is None or ischanage:
        print("缓存中没有数据，开始查询数据库……")
        articles = models.Article.objects.filter(author=author)
        print("数据库中查询到数据，同步到缓存中")
        cache.set("self_srticle", articles)

    return articles

