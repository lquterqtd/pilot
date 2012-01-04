#coding:utf-8
from pilot.info.models import SelfFeeContractInfo, CompanySponsoredContractInfo, SponsoredReceivablesInfo, CompanyInfo, ContractExecutedInfo

__author__ = 'lquterqtd'
from django.contrib import admin
from django.contrib.auth.models import User, Group
from pilot.info.models import SelfFeeStudent, ReceivablesInfo
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
        'remarks',
        'contract_id_link',
        'student_status',
        'training_phase',
        'actual_hours',
        'commercial_license',
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
    )
admin.site.register(SelfFeeStudent, SelfFeeStudentAdmin)
########################################################################
class SelfFeeContractInfoAdmin(admin.ModelAdmin):
    """"""
    list_display = (
        'get_student_name',
        'contract_id',
        'get_contract_amount',
        'available_hours',
        'actual_hours',
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