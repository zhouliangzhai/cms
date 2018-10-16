from django.contrib import admin


from . import  models


#列表zh装饰属性

class UserAdmin(admin.ModelAdmin):
    #列表显示属性
    list_display = ["name","nickname","age"]
    #列表过滤字段
    list_filter = ("age","name")
    # # 进行分页，每页3条数据
    # list_per_page = 3
    #直接编辑
    list_editable = ["age"]

    #修改框里能修改的属性值
    fields = ["name","age","nickname"]
    search_fields = ["age","nickname"]






admin.site.register(models.User,UserAdmin)
admin.site.register(models.Article,)
