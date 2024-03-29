from django.contrib import admin
from message.models import *

@admin.register(accident_Application)
class accident_Application_Admin(admin.ModelAdmin):
    list_display =  ('applicationID' ,'tableID','state','compensation_money')

@admin.register(compensate_Records)
class compensate_Records_Admin(admin.ModelAdmin):
    list_display =  ('tableID','startTime', 'count')

@admin.register(user_login)
class user_login_Admin(admin.ModelAdmin):
    list_display = ('id', 'power','password','email','telephone')

# Register your models here.
admin.site.register([products,trade_records,profit,table,applicant,recognizee_Infor,realtionship,complainInfor,Img,applicant_real])
