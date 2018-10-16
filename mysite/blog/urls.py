from django.conf.urls import url

from . import views

# app_name = "blog"

urlpatterns = [
    url(r"^index/$", views.index, name="index"),
    url(r"^add_user/$", views.add_user, name="add_user"),
    # url(r"^delete_user/$", views.delete_user, name="delete_user"),
    # url(r"^(\d+)/delete_user/$", views.delete_user, name="delete_user"),
    url(r"^delete_user/(?P<user_id>\d+)/$", views.delete_user, name="delete_user"),
    url(r"^list_user/$", views.list_user, name="list_user"),
    url(r"^reg/$", views.reg, name="reg"),
    url(r"^login/$", views.login, name="login"),
    url(r"^logout/$", views.logout, name="logout"),
    url(r"^show/(\d+)/$", views.show, name="show"),
    url(r"^(?P<u_id>\d+)/update/$", views.update, name="update"),

    url(r"^add_article/$", views.add_article, name="add_article"),
    url(r"^(?P<a_id>\d+)/delete_article/$", views.delete_article, name="delete_article"),
    url(r"^(?P<a_id>\d+)/update_article/$", views.update_article, name="update_article"),
    url(r"^(?P<a_id>\d+)/show_arcticle/$", views.show_arcticle, name="show_arcticle"),
    url(r"^self_article/$", views.self_article, name="self_article"),
    url(r"^code/$", views.code, name="code"),
    url(r"^(\w+)/checkusername/$", views.checkusername, name="checkusername"),

]
