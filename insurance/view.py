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
import decimal
from dateutil.relativedelta import relativedelta
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
	return render(request, 'test.html', LIST)

def getservices(request):
	LIST = {}
	if request.method == "GET":
		Dict = request.GET.dict()
		num = Dict.get('productID', None)
		if num != None:
			items = products.objects.filter(id = num)[:1]
			test = products.objects.filter(productID = num)[:1]
			if items.exists() and test.exists():
				LIST = model_to_dict(items[0])
				LIST.update(model_to_dict(test[0]))
				print(LIST)
				return render(request, 'services.html', LIST)
	if request.method == "POST":
		LIST = request.POST.dict()
		if LIST.get('measure') != None:
			LIST['answer'] = count_money2(LIST)
			return render(request, 'services.html', LIST)
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
		if Dao.exists():
			ID = Dao[0].id
			request.session['userid'] = ID
			request.session['user_name'] = Dao[0].email
			request.session['telephone'] = Dao[0].telephone
			request.session['power'] = Dao[0].power
			print(request.session.get('user_name', None))
			warning_give_money(request)
			create_compensate_Records(ID)
			return render(request, 'index.html', {'user_name': Dao[0].email})
		else:
			return render(request, 'login.html', {'error': '用户或密码错误'})
	return render(request, "login.html", LIST)

def random_verify(request):
    '''
    上传凭证并随机置死
    '''
    idcard = random.randint(1, 3)
    if idcard == 2:
        idcard = False
    else:
        idcard = True
    user = request.POST.get('user')
    ins = request.POST.get('ins')
    # ps = request.POST.get('password1')
    accident_Application.objects.create(
        applicationID=user,
        tableID=ins,
        accident_verify=idcard,
        compensation_money='1000'  # 一个默认金额
    )
    img = Img(img_url=request.FILES.get('img'))
    img.save()

def handling_deathqueue(userid, tableid):
    '''
    处理排队审核队列 【VIP优先 修改审核状态 合法进一步核算身故保险金】
    '''
    global userQue
    global vipQue
    forfeit_money = 2000
    state = {0: "line up", 1: "failed", 2: "approve"}
    applicantcase = applicant.objects.get(userID=userid)
    a_applicationcase = accident_Application.objects.get(tableID=tableid)

    # 没死:审核不通过
    if a_applicationcase.accident_verify == False:
        a_applicationcase.state = state.keys()[1]
        a_applicationcase.save()
    # 死了:身故申请加入排队队列
    else:
        if applicantcase.style == 1:  # 会员
            vipQue.put(tableid)
        else:
            userQue.put(tableid)
        a_applicationcase.state = state.keys()[0]
        a_applicationcase.save()
        # 处理排队队列
        if not vipQue.empty() or not userQue.empty():
            if not vipQue.empty():
                firsttableid = vipQue.get()
            else:
                firsttableid = userQue.get()
            a_applicationcase1 = accident_Application.objects.get(tableID=firsttableid)
            a_applicationcase1.state = state.keys()[2]

            tablecase = table.objects.get(tableID=firsttableid)
            tablecase.losestate = True  # 审核通过保单失效
            sum_money = tablecase.education_money
            sum_date = tablecase.losestate.year-tablecase.effectDate.year
            completed_date = trade_records.objects.filter(tableID=firsttableid).order_by('startTime')[-1].startTime.year
            rate = completed_date/sum_date   # 交费完成进度=交费完成日期/交费总日期
            a_applicationcase1.compensation_money = rate * sum_money

            tablecase.save()
            a_applicationcase1.save()

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
				power='0',
				money = '0',
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
			if sign == None:
				return render(request, '404.html')
			status = pay.verify(LIST, sign)
			print('post', status)
			if status:
				upload_trade_record(LIST, request)
				return render(request, 'finish_pay.html', LIST)
			else:
				return render(request, '404.html')
		except Exception as e:
			LIST['code_error'] = e.args
			return render(request, '404.html', LIST)
	else:
		LIST = request.POST.dict()
		sign = LIST.pop('sign', None)
		if sign == None:
				return render(request, '404.html')
		status = pay.verify(LIST, sign)
		print('get:', status)
		if status:
			upload_trade_record(LIST, request)
			return render(request, 'finish_pay.html', LIST)
		else:
			return render(request, '404.html')


#-----------KA tmp-----------#
def get_admin(request):
	ID = request.session.get('userid', None)
	if ID == None:
		return render(request, 'index.html')
	number = table.objects.filter(userID=ID, state=1)[:1]
	order = len(number)
	Applicant = applicant.objects.filter(userID = ID)[:1]
	relation = realtionship.objects.filter(userID = ID)[:1]
	user = user_login.objects.get(id=request.session.get('userid'))
	if Applicant.exists():
		LIST = {
			"name": Applicant[0].name,
			"idcard": Applicant[0].idcard,
			"address": Applicant[0].address,
			"order": order,
			"score":order*10,
			"rela":len(relation),
			"money": user.money,
		}
		return render(request, 'admin.html', LIST)
	else:
		LIST = {'applicant_state': '0'}
		return render(request, 'admin.html', LIST)

def producelist(request):
	return render(request, 'producelist.html')

def get_verify(request):
	if request.method == 'GET':
		return render(request, "verify.html")
	if request.method == 'POST':
		idcard = request.POST.get('idcard')
		name = request.POST.get('name')
		address = request.POST.get('address')
		print(address)
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
					return render(request, "admin.html")
				else:
					return render(request, "verify.html", {"error": "已有该信息"})
			return render(request, "admin.html")
		else:
			return render(request, "verify.html", locals())

def get_inform(request):
	ID = request.session.get('userid', None)
	if ID == None:
		return render(request, "admin.html")
	if request.method == "POST":
		method = request.POST.get('method', None)
		if request.POST.get('system', None):
			if method != '2':
				message = information.objects.filter(userid=ID, state=method, style="系统信息")
			else:
				message = information.objects.filter(userid=ID, style="系统信息")
			return render(request,'inform.html', {"LIST":message, "method": method})
		elif request.POST.get('method', None):
			if method != '2':
				message = information.objects.filter(userid=ID, state=method, style="支付信息")
			else:
				message = information.objects.filter(userid=ID, style="支付信息")
			return render(request,'inform.html', {"LIST":message, "method": method})
	elif request.method == "GET":
		method = request.GET.get('method', None)
		if method == '1':
			message = information.objects.filter(userid=ID, state=1)
			return render(request, 'inform.html', {"LIST": message, "method": 1})
		elif method == '0':
			message = information.objects.filter(userid=ID, state=0)
			return render(request, 'inform.html', {"LIST": message, "method": 0})
	message = information.objects.filter(userid=ID)
	return render(request, "inform.html", {"LIST": message, "method": 2})

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
			state = '0',
		)
		return render(request, "complain.html", {"inform": "投诉成功"})
	return render(request, "complain.html")

def get_compensate(request):
	ID = request.session.get('userid', None)
	if ID == None:
		return render(request, "index.html")
	accident_Set = accident_Application.objects.filter(applicationID = ID)
	LIST = []
	print(accident_Set)
	for Obj in accident_Set:
		tmp = model_to_dict(Obj)
		item = table.objects.get(id=Obj.tableID, userID=ID)
		tmp.update(model_to_dict(item))
		LIST.append(tmp)
	print(LIST)
	return render(request, "compensate.html", {"LIST": LIST})

def pay(request):
	"""
	不是界面但是支付中转，为了使得逻辑简洁
	"""
	if request.method == "POST":
		DICT = request.POST.dict()
		print(DICT)
		try:
			if DICT['cycle'] == "单次":
				delta = relativedelta(days = 0)
			elif DICT['cycle'] == "周交":
				delta = relativedelta(years = -1)
			elif DICT['cycle'] == "月交":
				delta = relativedelta(years = -3)
			table_num = table.objects.filter(productsID = DICT["productID"], userID = request.session.get("userid", None),
			 recognizee_ID = DICT["recognizee"], state = 1)
			if table_num.exists():
				return render(request, "404.html", {"code_error": "已经购买过该保单"})
			time = datetime.datetime.today() - delta
			table.objects.create(
				productsID = DICT["productID"],
				userID = request.session.get("userid", None),
				recognizee_name = DICT["name"],
				recognizee_ID = DICT["recognizee"],
				payCycle = DICT["cycle"],
				money = DICT["number"],
				state = 0,
				education_money=DICT["return_money"],
				loseDate = time,
			)
			table_num = table.objects.filter(loseDate = time)
			if table_num.exists():
				paytool = alipay.get_payment()
				total_num = 100 + len(trade_records.objects.all())
				print(DICT["productID"], table_num[0].id, DICT["number"])
				url = paytool.get(DICT["productID"], str(table_num[0].id) + ' ' + str(total_num), DICT["number"])
				title = "请按时付款保单号%s的保单" % table_num[0].id
				print(len(url))
				information.objects.create(
		            	userid=request.session.get("userid", None),
		            	style="支付信息",
		            	msg= url,
		            	title= title,
		            	state=0,
		            )
				return redirect(url)
		except Exception as e:
			return render(request, "404.html", {"code_error": e.args})
	return render(request, "admin.html")

def get_mytable(request):
	ID = request.session.get('userid', None)
	if ID == None:
		return render(request, '404.html')
	items = table.objects.filter(userID = ID)
	LIST = []
	print(items)
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
				LIST['return_money'] = LIST['education_money']
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
				LIST['return_money'] = count_money2(LIST)
				print(LIST)
				return render(request, "table_detail.html", LIST)
	return render(request, "404.html", {"code_error":"不能直接访问"})

def get_relationship(request):
	if request.session.get('userid', False) != False:
		if request.method == "POST":
			msg = request.POST.getlist('deleitem', None)
			for i in msg:
				realtionship.objects.get(recognizee_ID = i, userID = request.session.get('userid')).delete()
		elif request.GET.get('userID', False):
			realtionship.objects.get(userID=request.session.get('userid'), recognizee_ID = request.GET.get('userID')).delete()
		items = realtionship.objects.filter(userID = request.session.get('userid'))
		if items.exists():
			LIST = []
			for i in items:
				items2 = recognizee_Infor.objects.get(userID = i.recognizee_ID)
				LIST.append(items2)
			print(LIST)
			return render(request, "relationship.html", {"LIST": LIST})
	else:
		return render(request, "index.html")
	return render(request, "relationship.html")

def get_add_recognizee(request):
	if request.method == 'POST' and request.session.get('userid', False) != False:
		idcard = request.POST.get('idcard')
		name = request.POST.get('name')
		if applicant_real.objects.filter(userID = idcard, name = name)[:1].exists() == True:
			if not recognizee_Infor.objects.filter(userID = idcard)[:1].exists():
				recognizee_Infor.objects.create(
					name = name,
					userID = idcard,
				)
			if not realtionship.objects.filter(recognizee_ID = idcard, userID = request.session.get('userid'))[:1].exists():
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


def apply_compensate1(request):
	ID = request.session.get('userid', None)
	if ID == None:
		return render(request, 'index.html')
	items = table.objects.filter(userID = ID, state = True)
	LIST = []
	for i in items:
		tmp = model_to_dict(i)
		conn = products.objects.get(id = i.productsID)
		conn = model_to_dict(conn)
		conn.update(tmp)
		LIST.append(conn)
	print(LIST)
	return render(request, "compensate1.html", {"LIST": LIST})

def apply_compensate2(request):
	if request.method == "POST":
		return render(request, 'index.html')
	DICT = request.GET.dict()
	print(DICT)
	if DICT.get('userid', False) and DICT.get('tableid', False):
		return render(request, 'compensate2.html', DICT)
	return render(request, '404.html')

def apply_compensate3(request):
	if request.method == "GET":
		return render(request, "index.html")
	state = random.randint(1,3)
	if state == 2:
		state = True
	else:
		state = False
	userid = request.POST.get('userid')
	tableid = request.POST.get('tableid')
	money = request.POST.get('money')
	imgfile = request.FILES.get('img')
	print(imgfile.name)
	print(imgfile)
	accident_Application.objects.create(
			applicationID = userid,
			tableID = tableid,
			state = state,
			compensation_money = money,
			accident_verify = request.POST.get('describe'),
			image = imgfile,
			image_src = imgfile.name,
		)
	return render(request, 'compensate3.html')

def get_inform_detail(request):
	if request.method == "GET" and request.GET.get('id', None) != None:
		ID = request.GET.get('id', None)
		LIST = information.objects.get(id=ID)
		LIST.state = 1
		LIST.save()
	return render(request, 'inform_detail.html', {"LIST": LIST})

#end 视图

#----------逻辑------------#
#在逻辑这最好写上逻辑功能
#

def upload_trade_record(LIST, request):
	"""
	上传交易记录
	"""
	if not trade_records.objects.filter(tableID=LIST['out_trade_no'], trade_money=LIST['total_amount']).exists():
		conn = trade_records()
		conn.tableID = LIST['out_trade_no'].split(' ')[0]
		ID = conn.tableID
		conn.trade_money = LIST['total_amount']
		conn.userID = request.session.get('userid', None)
		conn.save()
		conn = table.objects.get(id=ID)
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

    pM = {"周交": 0, "月交": 1, "单次": 2}
    dL = {"三年": 3, "五年": 5, "十八年": 0}

    productsid = LIST['productID']
    if LIST.get('cycle', None):
    	pM_key = pM.get(LIST['cycle'], None)
    else:
    	pM_key = pM.get(LIST['payCycle'], None)
    dL_key = dL.get(LIST['deadline'])
    money = LIST['number']
    print(productsid, pM_key, dL_key, money)
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
    try:
	    if pM_key == 0:
	        sum_money = dL_value * 52 * money
	    elif pM_key == 1:
	        sum_money = dL_value * 12 * money
	    else:
	        sum_money = money
    except Exception as e:
    	sum_money = money
    returncase = profit.objects.filter(productsID=productsid, deadLine=dL_key, payMethod=pM_key)[:1]
    if returncase.exists():
    	returncase = returncase[0].Returen
    else:
    	returncase = decimal.Decimal(0.35)
    account_value = decimal.Decimal(sum_money) * decimal.Decimal(0.85)
    answer = account_value * (1 + returncase)
    answer = round(answer, 1)
    answer = str(answer)
    return answer


def create_compensate_Records(userid):
    """
    发钱【用户登录之后，检查可发钱保单并发钱，存对应一条理赔记录】
    """
    if userid == None:
    	return
    table_list = table.objects.filter(userID=userid)
    for tablecase in table_list:
        if tablecase.state == True:    # 保单有效
            #------------ # effectDate = tablecase.effectDate.year - tablecase.loseDate.year   # 处理年份# payCycle = tablecase.get_payMethod_display()
            today = datetime.datetime.now()
            if today > tablecase.loseDate:   # 已交完钱 发教育金
                tableid = tablecase.pk
                education_money = tablecase.education_money
                education_money = round(education_money,0)
                user = user_login.objects.get(id=userid)
                user.money = str(int(user.money) + int(education_money))
                user.save()
                compensate_Records.objects.create(
                    tableID=tableid,
                    count=education_money,
                    userid = userid,
                )
                tablecase.state = False  # 发完钱保单失效
                tablecase.save()


def payment(tablecase):
    '''
    用户交钱
    '''
    pM = {"周交":7, "月交":30, "单次": -1}
    tableid = tablecase.id
    cycle_day = pM[tablecase.payCycle]
    if cycle_day == -1:
    	return -1
    today = datetime.datetime.now()
    recent_day = trade_records.objects.filter(tableID=tableid).order_by('-startTime')[0].startTime
    minus_day = (today - recent_day).days
    if (tablecase.state is True) and (cycle_day > 0) and (minus_day >= cycle_day):  # 保单有效 + 2交费方式 + 到可以交费日期
        if minus_day == cycle_day:           # 不缺 今日=交钱日期
            pay_money = tablecase.money
            return pay_money
            # return render(request, 'finish_pay.html', pay_money)
        elif minus_day >= 2*cycle_day:
            if minus_day == 2 * cycle_day:   # 缺一次 今日=推迟交钱日期
                pay_money = 2*tablecase.money
                return  pay_money
                # return render(request, 'finish_pay.html', pay_money)  # 给交钱界面 显示交钱金额
            else:                            # 保单失效
                tablecase.state = False
                tablecase.save()
                return -1
    return -1


def warning_give_money(request):
    '''
    提醒交费
    '''
    userid = request.session.get('userid',None)
    if userid != None:
	    DAOTable = table.objects.filter(userID=userid, state = 1).order_by("effectDate")
	    pay = alipay.get_payment()
	    for i in DAOTable:
	        if datetime.datetime.now() > i.loseDate:
	        	continue
	        pay_money = payment(i)
	        print(pay_money)
	        if pay_money != -1:
	        	title = "保单号%s的保单已到期请付款，请按时付款" % i.id
	        	total_num = 100 + len(trade_records.objects.all())
	        	url = pay.get(i.id, str(i.id) + ' ' + str(total_num), i.money)
	        	if not information.objects.filter(userid=userid, msg= url).exists():
		            information.objects.create(
		            	userid=userid,
		            	style="支付信息",
		            	msg= url,
		            	title= title,
		            	state=0,
		            )

#end 逻辑
