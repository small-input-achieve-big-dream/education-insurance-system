# _*_ coding:utf-8 _*_
from django.db import models
import django.utils.timezone as timezone
import datetime
#python manage.py runserver 127.0.0.1:8080 启动服务器
#http://127.0.0.1:8080/admin/ 进入管理员界面
#python manage.py createsuperuser 创建管理员（admin ,1059117321）


# Create your models here
#django 框架提供ORM
#创造数据表 定义模型类
#进行数据迁移


#理赔记录表
class compensate_Records(models.Model):
	#投保人ID
	userid = models.CharField(max_length = 30)
	#理赔ID
	compensateID = models.IntegerField()
	#保单ID
	tableID = models.IntegerField()
	#订单创建时间
	startTime = models.DateTimeField(default = datetime.datetime.now)
	#订单修改时间
	changeTime = models.DateTimeField(auto_now = True)
	#经办人ID
	changerID = models.IntegerField()
	#修改内容
	content = models.CharField(max_length = 60)
	#发放教育金额
	count = models.IntegerField()
	class Meta:
		db_table = "compensate_Records"

#身故申请表
class accident_Application(models.Model):
	#申请ID
	applicationID = models.IntegerField()
	#保单ID
	tableID = models.IntegerField()
	#身故描述
	accident_verify = models.CharField(max_length = 200)
	#身故证明(图片形式)
	image = models.ImageField(upload_to='static')
	#审批状态
	state = models.BooleanField()	
	#身故保险金
	compensation_money = models.IntegerField()
	class Meta:
		db_table = "accident_Application"

#保险产品表
class products(models.Model):
	#产品名
	productsName = models.CharField(max_length = 30)
	#产品类型
	productsStyle = models.CharField(max_length = 30)
	#产品描述
	productsDes = models.CharField(max_length = 60)
	#投保人年龄范围
	age_range = models.CharField(max_length = 60)
	#被保人年龄范围
	recognizee_age_range = models.CharField(max_length = 60)
	#保险期限
	date = models.CharField(max_length = 60)
	#已成交单数
	dealCount = models.IntegerField()
	class Meta:
		db_table = "products"

#交易记录表
class trade_records(models.Model):
	#用户ID
	userID = models.CharField(max_length = 30)
	#保单ID
	tableID = models.CharField(max_length = 30, unique = True)
	#交易金额
	trade_money = models.CharField(max_length = 30)
	#创建时间
	startTime = models.DateTimeField(default = datetime.datetime.now)
	class Meta:
		db_table = "trade_records"

#保险收益明细表
class profit(models.Model):
	#产品ID
	productsID = models.IntegerField()
	#保险期限
	deadline = models.CharField(max_length = 30)
	#单次交费回报率
	oneReturen = models.IntegerField()
	#周交费回报率
	weekReturen = models.IntegerField()
	#月交费回报率
	monthReturn = models.IntegerField()
	class Meta:
		db_table = "profit"

#保单表
class table(models.Model):
	#产品ID
	productsID = models.IntegerField()
	#用户ID
	userID = models.CharField(max_length = 30)
	#被投保人姓名
	recognizee_name = models.CharField(max_length = 30)
	#被投保人身份证
	recognizee_ID = models.CharField(max_length = 30)
	#生效日期
	effectDate = models.DateTimeField(auto_now = datetime.datetime.now)
	#失效日期
	loseDate = models.DateTimeField(default = datetime.datetime.now)
	#交费周期
	payCycle = models.CharField(max_length = 30)
	#投入金额
	money = models.IntegerField()
	#状态
	state = models.BooleanField()
	class Meta:
		db_table = "table"

#用户登录表
class user_login(models.Model):
	#用户电话
	telephone = models.CharField(unique = True, max_length = 15)
	#用户邮箱
	email = models.EmailField(unique = True)
	#用户密码
	password = models.CharField(max_length = 60)
	#用户权限
	power = models.IntegerField()
	#上次查询时间
	changeTime = models.DateTimeField(default = datetime.datetime.now)
	class Meta:
		db_table = "user_login"

#投保人信息表
class applicant(models.Model):
	#用户ID
	userID = models.CharField(max_length = 30)
	#姓名
	name = models.CharField(max_length = 30)
	#身份证
	idcard = models.CharField(max_length = 30, unique = True)
	#类型
	style = models.IntegerField()
	#住址
	address = models.CharField(max_length = 200)
	#积分
	score = models.IntegerField()
	class Meta:
		db_table = "applicant"

#被保人信息报
class recognizee_Infor(models.Model):
	#身份证
	userID = models.CharField(max_length = 30, unique = True)
	#姓名
	name = models.CharField(max_length = 30)
	class Meta:
		db_table = "recognizee_Infor"

#投保人真实信息表
class applicant_real(models.Model):
	#身份证
	userID = models.CharField(max_length = 30, unique = True)
	#姓名
	name = models.CharField(max_length = 30)
	class Meta:
		db_table = "applicant_real"

#通信录
class realtionship(models.Model):
	# 用户ID
	userID = models.CharField(max_length = 30)
	# 被保人身份证
	recognizee_ID = models.CharField(max_length = 30)
	class Meta:
		db_table = "realtionship"

#投诉信息表
class complainInfor(models.Model):
	# 投诉人用户ID
	user_ID = models.CharField(max_length = 30)
	#原因
	reason = models.CharField(max_length = 30)
	# 投诉内容
	content = models.CharField(max_length = 300)
	# 状态
	state = models.BooleanField()
	# 处理人ID
	changerID = models.CharField(max_length = 30)
	# 反馈内容
	Return = models.CharField(max_length = 60)
	# 投诉时间
	startTime = models.DateTimeField(default = datetime.datetime.now)
	# 处理时间
	changeTime = models.DateTimeField(auto_now = True)
	class Meta:
		db_table = "complainInfor"

class Img(models.Model):
	img_url = models.ImageField(upload_to='static') # upload_to指定图片上传的途径，如果不存在则自动创建

class information(models.Model):
	#接收人
	userid = models.CharField(max_length = 30)
	#信息类型
	style = models.CharField(max_length = 20)
	#详细信息
	msg = models.CharField(max_length = 200)
	#标题
	title = models.CharField(max_length = 30)
	#发送时间
	createTime = models.DateTimeField(auto_now = True)
	class Meta:
		db_table = "information"
