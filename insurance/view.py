# -*- coding: utf-8 -*-

#--------包---------#
from django.shortcuts import render, redirect
from django.utils.datetime_safe import time
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
import random
from message.models import *
    #插入employee表

from django.shortcuts import HttpResponseRedirect,Http404,HttpResponse
from django.http import HttpResponse, JsonResponse

from django.shortcuts import HttpResponseRedirect,Http404,HttpResponse
from django.http import HttpResponse
from django.forms.models import model_to_dict

from message.alipay import alipay
import datetime

#--------视图-------#

def getIndex(request):
	LIST = {"title":"小投入成就大梦想"}
	DICT = {}
	if request.method == 'GET':
		DICT = request.GET.dict()
		action = DICT.pop('action', None)
		if action == 'logout':
			if request.session['userid']:
				del request.session['userid']
			if request.session['user_name']:
				del request.session['user_name']
			print('delete session')
	return render(request, 'index.html', LIST)

def getAbout_us(request):
	LIST = {"title":"关于我们"}
	return render(request, 'about-us.html', LIST)

def get404(request):
	LIST = {"title":"找不到页面"}
	return render(request, '404.html', LIST)

def gettest(request):	
	LIST = ['test1', 'test2']
	DICT = {'test3': '123', 'test4': '321'}
	return render(request, 'test.html', {'List': json.dumps(LIST), 'Dict': json.dumps(DICT)})
	# LIST = {"title":"测试"}
	# return render(request, 'test.html', LIST)

def getservices(request):
	LIST = {}
	if request.method == "GET":
		Dict = request.GET.dict()
		num = Dict.get('productID', None)
		if num != None:
			items = products.objects.filter(id = num)[:1]
			if items.exists():
				LIST = model_to_dict(items[0])
				LIST['productID'] = num
				return render(request, 'services.html', LIST)
	if request.method == "POST":
		LIST = request.POST.dict()
		if LIST.get('measure') != None:
			LIST['answer'] = count_money(LIST)
		elif LIST.get('buy') != None:
			LIST = {"productID": request.GET.get('productID', None)}
			if request.session.get('userid', False):
				ID = request.session.get('userid')
				items = realtionship.objects.filter(userID = ID)
				if items.exists():
					items = [i.recognizee_ID for i in items]
					items = [recognizee_Infor.objects.filter(userID = x)[:1][0] for x in items]
					LIST['LIST'] = items
				return render(request, 'tableform.html', LIST)
			else:
				return render(request, '404.html', {'code_error': '没有登录无法使用功能'})
	return render(request, '404.html', LIST)

def login(request):
	LIST = {}
	if request.method == 'POST':
		name = request.POST.get('user')
		pwd = request.POST.get('password')
		print(name, pwd)
		try:
			if '@' in name:
				Dao = user_login.objects.filter(email = name, password = pwd)[:1]
			else:
				Dao = user_login.objects.filter(telephone = name, password = pwd)[:1]
		except Exception as e:
			return render(request, 'login.html', {'error': '用户名格式不对'})
		print(Dao)
		if Dao.exists():
			ID = Dao[0].id
			request.session['userid'] = ID
			request.session['user_name'] = Dao[0].email
			request.session['telephone'] = Dao[0].telephone
			request.session['power'] = Dao[0].power
			print(request.session.get('user_name', None))
			return render(request, 'index.html', {'user_name': Dao[0].email})
		else:
			return render(request, 'login.html', {'error': '用户或密码错误'})
	return render(request, "login.html", LIST)

def givemoney(request):
	LIST = {}
	if request.method == 'GET':
		return render(request, "givemoney.html")
	if request.method == 'POST':

		idcard = random.randint(1,3)
		if idcard==2:
			idcard = True
		else:
			idcard = False
		user = request.POST.get('user')
		ins = request.POST.get('ins')
			# ps = request.POST.get('password1')
		accident_Application.objects.create(
				applicationID = user,
				tableID =ins,
				state =idcard,
				compensation_money='1000'
			)

		img = Img(img_url=request.FILES.get('img'))
		img.save()
		return  render(request, 'index.html')


def see(request):
	test = user_login.objects.all()
	return render(request, "see.html", locals())


def register(request):
	print(request.method)
	if request.method == 'GET':
		return render(request, "register.html")
	if request.method == 'POST':
		tel = request.POST.get('tel')
		em = request.POST.get('email')
		pwd = request.POST.get('password1')
		print(tel, em, pwd)
		Dao = user_login.objects.filter(Q(telephone=tel) | Q(email=em))
		print(Dao)
		if Dao.exists():
			return render(request, 'register.html', {'error': '用户已存在'})
		else:
			user_login.objects.create(
				telephone=int(tel),
				email=str(em),
				password=str(pwd),
				power='0'
			)
			return render(request, "login.html", locals())


def realname(request):

		LIST = {}
		idcard = user_login.objects.all()
		# user_loginList = user_login.objects.all()

		if request.method == 'GET':
			return render(request, "verify.html")
		if request.method == 'POST':
			real= request.POST.get('idcard')
			na = request.POST.get('name')
			ad = request.POST.get('address')

			if applicant_real.objects.filter(userID=real).exists() == True:
				if applicant_real.objects.filter(name=na).exists() == True:
					applicant.objects.create(
					name=na,
					userID=real,
					address=ad,
					style='0',
					score = '0'
				)
				test = user_login.objects.all()
				return render(request, "index.html", locals())
			else:
				return render(request, "verify.html", locals())


def get_finish_pay(request):
	pay = alipay.get_payment()
	if request.method == "GET":
		try:
			LIST = request.GET.dict()
			sign = LIST.pop('sign', None)
			status = pay.verify(LIST, sign)
			if status:
				upload_trade_record(LIST)
				return render(request, 'finish_pay.html', LIST)
			else:
				return render(request, '404.html')
		except Exception as e:
			LIST['code_error'] = e.args
			return render(request, '404.html', LIST)
	else:
		LIST = request.POST.dict()
		sign = LIST.pop('sign', None)
		status = pay.verify(LIST, sign)
		if status:
			upload_trade_record(LIST)
			return render(request, 'finish_pay.html', LIST)
		else:
			return render(request, '404.html')


#-----------KA tmp-----------#
def get_admin(request):
	ID = request.session.get('userid', None)
	if ID == None:
		return render(request, 'index.html')
	Applicant = applicant.objects.filter(userID = ID)[:1]
	if Applicant.exists():
		LIST = {
			"name": Applicant[0].name,
			"idcard": Applicant[0].idcard,
			"address": Applicant[0].address
		}
		return render(request, 'admin.html', LIST)
	else:
		LIST = {'applicant_state': '0'}
		return render(request, 'admin.html', LIST)

def get_verify(request):
	if request.method == 'GET':
		return render(request, "verify.html")
	if request.method == 'POST':
		idcard = request.POST.get('idcard')
		name = request.POST.get('name')
		address = request.POST.get('address')

		if applicant_real.objects.filter(userID = idcard).exists() == True:
			if applicant_real.objects.filter(name = name).exists() == True:
				if not applicant.objects.filter(idcard = idcard).exists():
					applicant.objects.create(
						userID = request.session.get('userid', None),
						name = name,
						idcard = idcard,
						address = address,
						style = '0',
						score = '0'
					)
				else:
					return render(request, "verify.html", {"error": 已有该信息})
			return render(request, "admin.html")
		else:
			return render(request, "verify.html", locals())

def get_inform(request):
	
	return render(request, "inform.html")

def get_complain(request):
	if request.method == 'POST':
		complainInfor.objects.create(
			user_ID = request.POST.get('userid'),
			reason = request.POST.get('reason'),
			content = request.POST.get('detail', "-"),
			state = 0,
			changerID = "None",
			Return = "-",
		)
		information.objects.create(
			userid = request.POST.get('userid'),
			style = "系统信息",
			msg = "您的投诉信息已经收获",
			title = "投诉成功",
		)
		return render(request, "complain.html", {"inform": "投诉成功"})
	return render(request, "complain.html")

def get_compensate(request):
	return render(request, "compensate.html")

def pay(request):
	"""
	不是界面但是支付中转，为了使得逻辑简洁
	"""
	if request.method == "POST":
		DICT = request.POST.dict()
		try:
			table.objects.create(
				productsID = DICT["productID"],
				userID = request.session.get("userid", None),
				recognizee_name = DICT["name"],
				recognizee_ID = DICT["recognizee"],
				payCycle = DICT["cycle"],
				money = DICT["number"],
				state = 0,
			)
			table_num = table.objects.filter(productsID = DICT["productID"], userID = request.session.get("userid", None),
			 recognizee_ID = DICT["recognizee"], payCycle = DICT["cycle"], money = DICT["number"])
			if table_num.exists():
				paytool = alipay.get_payment()
				url = paytool.get(DICT["name"], table_num[0].id, DICT["number"])
				return redirect(url)
		except Exception as e:
			print(e.args)
			return render(request, "admin.html")
	return render(request, "admin.html")

def get_mytable(request):
	ID = request.session.get('userid', None)
	if ID == None:
		return render('404.html')
	items = table.objects.filter(userID = ID)
	LIST = []
	for i in items:
		tmp = model_to_dict(i)
		conn = products.objects.get(id = i.productsID)
		tmp.update(model_to_dict(conn))
		LIST.append(tmp)
	print(LIST)
	return render(request, "mytable.html", {"LIST": LIST})

def get_mytrade(request):
	ID = request.session.get('userid', None)
	if ID == None:
		return render(request, '404.html')
	items = trade_records.objects.filter(userID = ID)
	LIST = []
	for i in items:
		tmp = model_to_dict(i)
		conn = table.objects.get(id = i.tableID)
		tmp.update(model_to_dict(conn))
		LIST.append(tmp)
	print(LIST)
	return render(request, "trade.html", {"LIST": LIST})

def get_tableform(request):
	return render(request, "tableform.html")

def get_showtable(request):
	if request.method == "GET":
		return render(request, "404.html")
	else:
		LIST = request.POST.dict()
		if LIST.get("recognizee_ID", False) and LIST.get("productID", False):
			user = table.objects.filter(productsID=LIST["productID"])[:1]
			product = products.objects.filter(id=LIST["productID"])[:1]
			if user.exists() and product.exists():
				LIST.update(model_to_dict(user[0]))
				LIST.update(model_to_dict(product[0]))
				print(LIST)
				return render(request, "showtable.html", LIST)
	return render(request, "showtable.html")

def get_table_detail(request):
	"""
	输入(productID, recognizee, userid) 
	输出整个页面
	"""
	if request.method == "POST":
		LIST = request.POST.dict()
		if LIST.get("recognizee", False) and LIST.get("productID", False):
			user = recognizee_Infor.objects.filter(userID=LIST["recognizee"])[:1]
			product = products.objects.filter(id=LIST["productID"])[:1]
			if user.exists() and product.exists():
				LIST.update(model_to_dict(user[0]))
				LIST.update(model_to_dict(product[0]))
				print(LIST)
				return render(request, "table_detail.html", LIST)
	return render(request, "404.html", {"code_error":"不能直接访问"})

def get_relationship(request):
	if request.session.get('userid', False) != False:
		if request.method == "POST":
			msg = request.POST.getlist('deleitem', None)
			for i in msg:
				realtionship.objects.filter(recognizee_ID = i).delete()
		items = realtionship.objects.filter(userID = request.session.get('userid'))
		if items.exists():
			LIST = []
			for i in items:
				items2 = recognizee_Infor.objects.filter(userID = i.recognizee_ID)
				LIST.append(items2)
			return render(request, "relationship.html", {"LIST": LIST})
	else:
		return render(request, "index.html")
	return render(request, "relationship.html")

def get_add_recognizee(request):
	if request.method == 'POST' and request.session.get('userid', False) != False:
		idcard = request.POST.get('idcard')
		name = request.POST.get('name')
		if applicant_real.objects.filter(userID = idcard).exists() == True:
			if applicant_real.objects.filter(name = name).exists() == True:
				if not recognizee_Infor.objects.filter(userID = idcard).exists():
					recognizee_Infor.objects.create(
						name = name,
						userID = idcard,
					)
				if not realtionship.objects.filter(recognizee_ID = idcard).exists():
					realtionship.objects.create(
						userID = request.session.get('userid'),
						recognizee_ID = idcard,
					)
			return render(request, "add_recognizee.html", locals())
		else:
			return render(request, "verify.html", locals())
	return render(request, "add_recognizee.html")

def get_smallinform(request):
	if request.session.get('userid', False) != False:
		items = user_login.objects.filter(id = request.session.get('userid'))
		if items.exists():
			items2 = information.objects.filter(createTime__range=(items[0].changeTime, datetime.datetime.now()))
			request.session['msg_num'] = len(items2)
		return render(request, "small_inform.html", {'LIST': items2})
	return render(request, "small_inform.html")


#end 视图

#----------逻辑------------#
#在逻辑这最好写上逻辑功能
#

def upload_trade_record(LIST):
	"""
	上传交易记录
	"""
	if not trade_records.objects.filter(tableID=LIST['out_trade_no'], trade_money=LIST['total_amount']).exists():
		conn = trade_records()
		conn.tableID = LIST['out_trade_no']
		conn.trade_money = LIST['total_amount']
		conn.userID = request.session.get('userid', None)
		conn.save()
		conn = table.objects.get(id=LIST['out_trade_no'])
		if conn != None:
			conn.state = True
			conn.save()
			print(conn.state)


def count_money(LIST):
	"""
	计算获益金额
	"""
	answer = 1
	answer = "金额: " + str(answer)
	return answer

def count_money2(LIST):
    """
    计算获益金额【用于保费测算和保单付款】
    """
    # pM = {"week": 0, "month": 1, "one time": 2}
    dL = {3: 3, 5: 5, 18: 0}
    productsid = LIST['productsID']
    pM_key = LIST['paymethod']
    dL_key = LIST['deadline']
    money = LIST['money']
    for key, value in dL.items():
        if dL_key == key:
            if value != 0:
                dL_value = value  # dL_value-交费年限
            else:
                birth = LIST['recognizee'][6:13]
                birthday = datetime.datetime.strptime(birth, "%Y%m%d")
                today = datetime.datetime.now()
                dL_value = 18 + birthday.year - today.year
            break
    if pM_key == 0:
        sum_money = dL_value * 52 * money
    elif pM_key == 1:
        sum_money = dL_value * 12 * money
    else:
        sum_money = money
    returncase = profit.objects.get(productsID=productsid, deadLine=dL_key, payMethod=pM_key).Returen
    account_value = sum_money * 0.85
    answer = account_value * (1 + returncase)
    answer = "金额: " + str(answer)
    return answer
# def create_table()
# 	pass

#end 逻辑
