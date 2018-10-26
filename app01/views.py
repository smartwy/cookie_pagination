from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
# mark_safe :把数据转为安全数据（一般用于用户ui获取到的数据判断为安全数据正常渲染与使用，否则django会对其进行安全操作）
from django.utils.safestring import mark_safe

# Create your views here.
import math
import random

LIST = []
for i in range(1010):
	LIST.append(i)

def index(request):
	rev = reverse('a-polls:index')
	print(request.path_info)
	print(rev)
	from django.core.handlers.wsgi import WSGIRequest
	for k,v in request.environ.items():
		print(k, ':', v)
	return render(request, 'index.html')

def tpl1(request):
	# 不影响参数变量的传递，先生成总体模板，在进行渲染
	rand = random.randint(32, 126)
	return  render(request, 'tpl1.html', {'name':'tpl-1', 'tag':'tag2', 't':'tag1', 'rand':rand})

def tpl2(request):

	return  render(request, 'tpl2.html', {'name':'tpl-2'})

def user_list(request):
	# 获取选中页码
	page = int(request.GET.get('p', 1))
	page_step = int(request.COOKIES.get('pa_nu', 10)) # 获取每页显示条数
	start = (page-1) * page_step
	end = page * page_step
	data = LIST[start:end] # 每页显示数量暂为20个
	# 获取总页码 也可使用 divmod(a,b)函数返回商数与余数
	page_max = math.ceil(len(LIST) / page_step) # 向上取整，5.1 = 6
	page_list = range(1, int(page_max) + 1) # 动态生成页码列表，range返回最大值与实际页码值差1，所以加一
	# 设置只显示11页,保持奇数页，
	display_page_sum = 11
	if page <= 5:
		page_list = page_list[0:display_page_sum] # 选中前5页的页码列表，只显示11页。注意：[]内是page_list的索引
	elif page_max - page <= (display_page_sum-1)/2:
		page_list = page_list[page_max - display_page_sum:page_max] # 选中后5页的页码列表，
	else:
		page_list = page_list[page - (display_page_sum+1)//2:page + (display_page_sum-1)//2] # 选中前5页至后5页的页码列表，
		# print(page_list)
	up_one_page = ''
	down_one_page = ''
	if page >= 1: # 如果是第一页没有上一页按键
		up_one_page = page - 1
	if page < page_max: # 取反，是最大页时没有下一页
		down_one_page = page + 1
	return render(request, 'user_list.html', {'li': data,
	                                          'page_list': page_list,
	                                          'page': page,
	                                          'page_max':page_max,
	                                          'up_one_page': up_one_page,
	                                          'down_one_page': down_one_page,
	                                          })


########################### cookie ###########################
# 模拟数据库数据
user_info = {
	'wy':{'pwd': "123"},
	'zg':{'pwd': "456"},
}
def clogin(request):
	if request.method == 'GET':
		return render(request, 'clogin.html')
	if request.method == 'POST':
		u = request.POST.get('username')
		p = request.POST.get('pwd')
		dic = user_info.get(u)
		if not dic:
			return render(request, 'clogin.html')
		if dic['pwd'] == p:
			res = redirect('/cindex/') # 重定向302
			res.set_cookie('cuser', u) # 把cookie数据加入到URL中
			# res.set_signed_cookie('cuser', u, salt='456abc') # cookie 加盐加密
			return res
		else:
			return render(request, 'clogin.html')
''' 
	response = render(request, '***.html')
	response = redirect('/***/')
	设置cookie,关闭浏览器就失效
	response.set_cookie('k', 'v')
	return response
	
	设置参数：
		 key,              键
        value='',         值
        max_age=None,     超时时间(超过这个时间，cookie自动失效，默认秒)
        expires=None,     超时时间(设置系统时间的偏移值，需要导入datetime模块)
        path='/',         Cookie生效的路径，/ 表示根路径，特殊的：跟路径的cookie可以被任何url的页面访问
        domain=None,      Cookie生效的域名
        secure=False,     https传输
        httponly=False    只能http协议传输，无法被JavaScript获取（不是绝对，底层抓包可以获取到也可以被覆盖）
'''
#################### 测试FBV装饰器 ####################
def auth(func):
	def inner(request, *args, **kwargs):
		v = request.COOKIES.get('cuser')
		if not v:
			return redirect('/clogin/')
		return func(request, *args, **kwargs)
	return inner

@auth # FBV 装饰器
def cindex(request):
	v = request.COOKIES.get('cuser')
	# # v = request.get_signed_cookie('cuser', salt='456abc') # 加盐解密
	# if not v:
	# 	return redirect('/clogin/')
	return render(request, 'cindex.html', {'current_user':v})

def order(request):
	v = request.COOKIES.get('cuser')
	# # v = request.get_signed_cookie('cuser', salt='456abc') # 加盐解密
	# if not v:
	# 	return redirect('/clogin/')
	return render(request, 'cindex.html', {'current_user':v})

#################### 测试CBV装饰器使用 ####################
from django import views
from django.utils.decorators import method_decorator # django 提供的类装饰器

@method_decorator(auth, name='dispatch') # 1、类加装饰器 对类下的所有方法使用auth装饰器(dispatch判断方法,所以需要传参)
class Order(views.View):

	@method_decorator(auth) # 2、类下函数加装饰器使用方法
	def get(self, request):
		v = request.COOKIES.get('cuser')
		return 	render(request, 'cindex.html', {'current_user':v})

	def post(self, request):
		v = request.COOKIES.get('cuser')
		return 	render(request, 'cindex.html', {'current_user':v})








