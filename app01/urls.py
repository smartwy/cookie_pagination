#!/usr/bin/python3
# -*- coding:utf-8 -*-
#Name:     
#Descripton:
#Author:    smartwy
#Date:     
#Version:

from  django.conf.urls import url
from app01 import views
'''
python3 Django 环境下，如果你遇到在根目录下urls.py中的include方法的第二个参数namespace添加之后就出错的问题。
请在[app_name]目录下的urls.py中的urlpatterns前面加上app_name='[app_name]'， [app_name]代表你的应用的名称。
例如：app_name ='[blog]' 
'''
app_name ='app01'
urlpatterns = [
	url(r'^index/', views.index, name='index'),
]


