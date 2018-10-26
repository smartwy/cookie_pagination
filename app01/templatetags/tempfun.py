#!/usr/bin/python3
# -*- coding:utf-8 -*-
#Name:     
#Descripton:
#Author:    smartwy
#Date:     
#Version:

from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag # 使用时：{% echo 参数 %}
def echo(arg):
	# print(type(arg))
	arg = chr(int(arg)) # 把数字转ASCII码
	return arg

@register.filter       # 使用时：{{ 参数|echo：参数 }} 注意：最多就两个参数，
def echo_f(na, arg):
	argl = arg.split() # 切分成多个参数，在传参时注意格式，split默认是空格，
	ar = str(argl[0])
	return na + arg + '， 后面是参数切出来的数据： ' + ar   # 必须是字符串


