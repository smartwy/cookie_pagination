"""cookie_pagination URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from app01 import views
'''
python3 Django 环境下，如果你遇到在根目录下urls.py中的include方法的第二个参数namespace添加之后就出错的问题。
请在[app_name]目录下的urls.py中的urlpatterns前面加上app_name='[app_name]'， [app_name]代表你的应用的名称。
例如：app_name ='[blog]' 
'''

urlpatterns = [
    # path('admin/', admin.site.urls),
    # url(r'^index/$', views.index),
    url(r'^a/', include('app01.urls', namespace='a-polls')), # 避免不同应用中的路由使用了相同的名字发生冲突，使用命名空间区别开
    url(r'^b/', include('app01.urls', namespace='b-polls')),
    url(r'^tpl1', views.tpl1), # 模板1
    url(r'^tpl2', views.tpl2), # 模板2
    url(r'^user_list', views.user_list), # 分页
    url(r'^clogin', views.clogin), # cookie
    url(r'^cindex', views.cindex), # cookie/ FBV装饰器
    url(r'^order', views.Order.as_view()), # CBV装饰器
]
