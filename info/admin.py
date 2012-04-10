#coding:utf-8
from pilot.info.models import SelfFeeContractInfo, CompanySponsoredContractInfo, SponsoredReceivablesInfo, CompanyInfo, ContractExecutedInfo

__author__ = 'lquterqtd'
from django.contrib import admin
from django.contrib.auth.models import User, Group
from pilot.info.models import SelfFeeStudent, ReceivablesInfo
import datetime

admin.site.unregister(User)
admin.site.unregister(Group)
########################################################################
class ReceivablesInfoInline(admin.TabularInline):
    """"""
    model = ReceivablesInfo
    extra = 0
########################################################################
class SponsoredReceivablesInfoInline(admin.TabularInline):
    """"""
    model = SponsoredReceivablesInfo
    extra = 0
########################################################################
from django.contrib.admin.views.main import ChangeList
class MyChangList(ChangeList):
    """"""
    def get_results(self, request):
        user = request.user
        qs = self.query_set
        if user.username == 'editor':
            #self.list_display.remove('remarks')
            #self.list_editable = ('actual_hours',)
            self.list_display = (
                'student_number',
                'name',
                'actual_hours',
                'get_update_time',
            )
        elif user.username == 'confirm':
            self.list_display = (
                'student_number',
                'name',
                'actual_hours',
                'get_update_time',
                'is_confirmed',
            )
        self.query_set = qs
        return super(MyChangList, self).get_results(request)
########################################################################
class SelfFeeStudentAdmin(admin.ModelAdmin):
    """"""
    list_display = (
        'student_number',
        'name',
        'gender',
        'education' ,
        'get_school_time',
        'student_type',
        'grade',
        #'remarks',
        'contract_id_link',
        'student_status',
        'training_phase',
        'get_actual_hours',
        'get_update_time',
        'get_confirmed_info',
        )
    fieldsets = [
        ('学员基本信息', {'fields': [
            'student_number',
            'name',
            'gender',
            'id_number',
            'tel',
            'graduated_from',
            'education' ,
            'school_time_year',
            'school_time_month',
            'student_type',
            'company',
            'grade',
            'remarks',
            'contract_id',
            'training_outline',
            'student_status',
            'training_phase',
            'actual_hours',
            'commercial_license',
            'is_confirmed',
            #'actual_hours_update_time',
        ]}),
    ]
    search_fields = (
        'name',
    )

    list_filter = (
        'school_time_year',
        'student_type',
        'grade',
        'student_status',
        'training_phase',
        'commercial_license',
        'is_confirmed'
    )
    list_per_page = 50
    #----------------------------------------------------------------------
    def get_changelist(self, request, **kwargs):
        """"""
        return MyChangList
    #----------------------------------------------------------------------
    def save_model(self, request, obj, form, change):
        """"""
        if request.user.username == 'editor':
            obj.is_confirmed = False
            obj.actual_hours_update_time = datetime.datetime.now()
        obj.save()
admin.site.register(SelfFeeStudent, SelfFeeStudentAdmin)
########################################################################
class SelfFeeContractInfoAdmin(admin.ModelAdmin):
    """"""
    list_display = (
        'get_student_name',
        'contract_id',
        'get_contract_amount',
        'available_hours',
        'get_actual_hours',
        'is_over_plan_hours',
        'have_received_amount',
        'get_arrears_info',
    )

    inlines = [ReceivablesInfoInline]
admin.site.register(SelfFeeContractInfo, SelfFeeContractInfoAdmin)
########################################################################
class CompanySponsoredContractInfoAdmin(admin.ModelAdmin):
    """"""
    list_display = (
        'get_company_name',
        'contract_id',
        'get_executed_info',
        'get_students_count',
        'get_contract_amount',
        'have_received_amount',
        'get_arrears_info',
        )

    inlines = [SponsoredReceivablesInfoInline]
admin.site.register(CompanySponsoredContractInfo, CompanySponsoredContractInfoAdmin)
########################################################################
class ContractExecutedInfoAdmin(admin.ModelAdmin):
    """"""
    list_display = (
        'get_company_name',
        'contract_id',
        'contract_cycle',
        'theory_date',
        'flight_date',
        'is_overdue'
    )
admin.site.register(ContractExecutedInfo, ContractExecutedInfoAdmin)
admin.site.register(CompanyInfo)
