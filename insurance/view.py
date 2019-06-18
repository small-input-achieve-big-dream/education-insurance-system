#--------包---------#
from django.shortcuts import render, redirect
from django.utils.datetime_safe import time
from django.views.decorators.csrf import csrf_exempt
import json
import random
from message.models import *
    #插入employee表

from django.shortcuts import HttpResponseRedirect,Http404,HttpResponse,render_to_response
from django.http import HttpResponse, JsonResponse

from django.shortcuts import HttpResponseRedirect,Http404,HttpResponse
from django.http import HttpResponse
from django.forms.models import model_to_dict

from message.alipay import alipay


#--------视图-------#
def getIndex(request):
	LIST = {"title":"小投入成就大梦想"}
	LIST['user_name'] = request.session.get('user_name', '')
	print(LIST)
	return render(request, 'index.html', LIST)

def getAbout_us(request):
	LIST = {"title":"关于我们"}
	LIST['user_name'] = request.session.get('user_name', '')
	return render(request, 'about-us.html', LIST)

def get404(request):
	LIST = {"title":"找不到页面"}
	LIST['user_name'] = request.session.get('user_name', '')
	return render(request, '404.html', LIST)

def gettest(request):	
	LIST = {"title":"测试"}
	LIST['user_name'] = request.session.get('user_name', '')
	return render(request, 'test.html', LIST)

def getservices(request):
	LIST = {}
	LIST['user_name'] = request.session.get('user_name', '')
	if request.POST:
		LIST = request.POST.dict()
		if LIST.get('measure') != None:
			LIST['answer'] = count_money(LIST)
		elif LIST.get('buy') != None:
			url = ''
			# url = alipay.get_payment(name = , num = , account = LIST['money'])
			return redirect(url)
	return render(request, 'services.html', LIST)

def login(request):

	# user_loginList = user_login.objects.all()
	# # user_loginList = user_login.objects.get(id=2)
	# return  render_to_response("login.html",locals())
	# return render(request,'login.html',{"title":"登录",'user_login':user_loginList})


	LIST = {}
	LIST['user_name'] = request.session.get('user_name', '')
	if request.method == 'POST':
		name = request.POST.get('user')
		pwd = request.POST.get('pw')
		Dao = user_login.objects.filter(email=name, password=pwd)[:1]
		if Dao.exists():
			ID = Dao[0].id
			request.session['userid'] = ID
			request.session['user_name'] = name
			return render(request, 'index.html')
		else:
			return render(request, 'login.html', {'error': '用户或密码错误'})
	return render(request, "login.html", LIST)

def givemoney(request):

    sava_path = 'static/images/logo/logo.png'  # 默认图片
	# return render_to_response('givemoney.html')
    if request.method == 'POST':
        files = request.FILES.get('file')  # 获取图片
        filename ='test'
        sava_path = 'static/images/'

        # 将图片分段读取并写入文件
        with open(sava_path, 'wb') as f:
            for file in files.chunks():
                f.write(file)
                f.flush()
        # 将图片路径更新到当前用户的表中
        user = accident_Application.objects.filter(token=request.COOKIES.get('token'))
        user.update(icon=sava_path)
    # # 将上传成功的图片路径返回给页
    return render(request, 'givemoney.html')
    # return JsonResponse({'img': sava_path})



def register(request):
	LIST = {}
	LIST['user_name'] = request.session.get('user_name', '')
	idcard  = user_login.objects.all()
	if request.method == 'GET':
		return render(request, "register.html")
	if request.method == 'POST':
		qq = request.POST.get('tel')
		em = request.POST.get('email')
		ps = request.POST.get('password1')
		user_login.objects.create(
				telephone=qq,
				email=  em,
				password= ps,
				power='0'
		)
		return render(request, "login.html", locals())


def get_finish_pay(request):
	LIST = {}
	LIST['user_name'] = request.session.get('user_name', '')
	try:
		LIST['total_amount'] = request.GET['total_amount']
		LIST['timestamp'] = request.GET['timestamp']
		LIST['out_trade_no'] = request.GET['out_trade_no']
		upload_trade_record(LIST)
		return render(request, 'finish_pay.html', LIST)
	except Exception as e:
		LIST['code_error'] = e.args
		return render(request, '404.html', LIST)

#end 视图

#----------逻辑------------#
#在逻辑这最好写上逻辑功能
#

def upload_trade_record(LIST):
	"""
	上传交易记录
	"""
	conn = trade_Records()
	conn.tableID = LIST['out_trade_no']
	conn.trade_money = LIST['total_amount']
	conn.save()


def count_money(LIST):
	"""
	计算获益金额
	"""
	answer = 1
	answer = "金额: " + str(answer)
	return answer

# def create_table()
# 	pass

#end 逻辑
