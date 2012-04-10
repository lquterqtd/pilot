#coding:utf-8
from django.http import HttpResponse, HttpResponseRedirect
# Create your views here.
#----------------------------------------------------------------------
from django.shortcuts import render_to_response
from info.forms import ReportDateSelectForm
from info.models import CompanyInfo, CompanySponsoredContractInfo, SponsoredReceivablesInfo, ReceivablesInfo, SelfFeeStudent, SelfFeeContractInfo
#----------------------------------------------------------------------
def get_plan_list(StartDate, EndDate):
    """"""
    p = ReceivablesInfo.objects.filter(plan_date__gte=StartDate).filter(plan_date__lte=EndDate)
    plan_sum = 0.0
    list_cid = []
    for item in p:
        plan_sum += item.plan_amount
        list_cid.append(item.contract_id)
    list_cid = list(set(list_cid))
    report_plan_list = []
    for item_pk in list_cid:
        #获取收款所对应的合同
        c_id = SelfFeeContractInfo.objects.get(pk=item_pk)
        #获取合同所对应的学员
        student_info = SelfFeeStudent.objects.get(contract_id=c_id.contract_id)
        p = ReceivablesInfo.objects.filter(contract=c_id.pk).filter(plan_date__gte=StartDate).filter(plan_date__lte=EndDate)
        for item in p:
            report_plan_list.append(
                    {
                    'id': student_info.student_number,
                    'name': student_info.name,
                    'contract_id': student_info.contract_id,
                    'plan': item.plan_amount,
                    'date': item.plan_date,
                    }
            )
    report_plan_list.sort(key = lambda x:x['date'])
    return plan_sum, report_plan_list
#----------------------------------------------------------------------
def get_actual_list(StartDate, EndDate):
    """"""
    p = ReceivablesInfo.objects.filter(actual_date__gte=StartDate).filter(actual_date__lte=EndDate)
    actual_sum = 0.0
    list_cid = []
    for item in p:
        actual_sum += item.actual_amount
        list_cid.append(item.contract_id)
    list_cid = list(set(list_cid))
    report_actual_list = []
    for item_pk in list_cid:
        #获取收款所对应的合同
        c_id = SelfFeeContractInfo.objects.get(pk=item_pk)
        #获取合同所对应的学员
        student_info = SelfFeeStudent.objects.get(contract_id=c_id.contract_id)
        p = ReceivablesInfo.objects.filter(contract=c_id.pk).filter(actual_date__gte=StartDate).filter(actual_date__lte=EndDate)
        for item in p:
            report_actual_list.append(
                    {
                    'id': student_info.student_number,
                    'name': student_info.name,
                    'contract_id': student_info.contract_id,
                    'plan': item.actual_amount,
                    'date': item.actual_date,
                    }
            )
    report_actual_list.sort(key = lambda x:x['date'])
    return actual_sum, report_actual_list
def report(request):
    """"""
    if request.method == 'POST':
        form = ReportDateSelectForm(request.POST)
        if form.is_valid():
            #return HttpResponseRedirect('/admin/report')
            StartDate = form.cleaned_data['StartDate']
            EndDate = form.cleaned_data['EndDate']
            plan_sum, report_plan_list = get_plan_list(StartDate, EndDate)
            actual_sum, report_actual_list = get_actual_list(StartDate, EndDate)
            return render_to_response(
                'admin/report.html',
                {
                    'form': form,
                    'plan_sum': plan_sum,           #应收款总和
                    'actual_sum': actual_sum,       #实收款总和
                    'StartDate': StartDate,         #起始日期
                    'EndDate': EndDate,             #终止日期
                    'flag': True,                   #是否要显示结果
                    'report_plan_list': report_plan_list,
                    'report_actual_list': report_actual_list,
                }
            )
    else:
        form = ReportDateSelectForm()

    return render_to_response(
        'admin/report.html',
        {
        'form': form,
        }
    )
#----------------------------------------------------------------------
def company_get_plan_list(StartDate, EndDate):
    """"""
    p = SponsoredReceivablesInfo.objects.filter(plan_date__gte=StartDate).filter(plan_date__lte=EndDate)
    plan_sum = 0.0
    list_cid = []
    for item in p:
        plan_sum += item.plan_amount
        list_cid.append(item.contract_id)
    list_cid = list(set(list_cid))
    report_plan_list = []
    for item_pk in list_cid:
        #获取收款所对应的合同
        c_id = CompanySponsoredContractInfo.objects.get(pk=item_pk)
        #获取合同所对应的学员
        company_info = CompanyInfo.objects.get(pk=c_id.company_id)
        p = SponsoredReceivablesInfo.objects.filter(contract=c_id.pk).filter(plan_date__gte=StartDate).filter(plan_date__lte=EndDate)
        for item in p:
            report_plan_list.append(
                    {
                    'company_name': company_info.company_name,
                    'contract_id': c_id.contract_id,
                    'plan': item.plan_amount,
                    'date': item.plan_date,
                    }
            )
    report_plan_list.sort(key = lambda x:x['date'])
    return plan_sum, report_plan_list
#----------------------------------------------------------------------
def company_get_actual_list(StartDate, EndDate):
    """"""
    p = SponsoredReceivablesInfo.objects.filter(actual_date__gte=StartDate).filter(actual_date__lte=EndDate)
    actual_sum = 0.0
    list_cid = []
    for item in p:
        actual_sum += item.actual_amount
        list_cid.append(item.contract_id)
    list_cid = list(set(list_cid))
    report_actual_list = []
    for item_pk in list_cid:
        #获取收款所对应的合同
        c_id = CompanySponsoredContractInfo.objects.get(pk=item_pk)
        #获取合同所对应的学员
        company_info = CompanyInfo.objects.get(pk=c_id.company_id)
        p = SponsoredReceivablesInfo.objects.filter(contract=c_id.pk).filter(actual_date__gte=StartDate).filter(actual_date__lte=EndDate)
        for item in p:
            report_actual_list.append(
                    {
                    'company_name': company_info.company_name,
                    'contract_id': c_id.contract_id,
                    'plan': item.actual_amount,
                    'date': item.actual_date,
                    }
            )
    report_actual_list.sort(key = lambda x:x['date'])
    return actual_sum, report_actual_list
#----------------------------------------------------------------------
def company_report(request):
    """"""
    if request.method == 'POST':
        form = ReportDateSelectForm(request.POST)
        if form.is_valid():
            StartDate = form.cleaned_data['StartDate']
            EndDate = form.cleaned_data['EndDate']
            plan_sum, report_plan_list = company_get_plan_list(StartDate, EndDate)
            actual_sum, report_actual_list = company_get_actual_list(StartDate, EndDate)
            return render_to_response(
                'admin/company_report.html',
                    {
                    'form': form,
                    'plan_sum': plan_sum,           #应收款总和
                    'actual_sum': actual_sum,       #实收款总和
                    'StartDate': StartDate,         #起始日期
                    'EndDate': EndDate,             #终止日期
                    'flag': True,                   #是否要显示结果
                    'report_plan_list': report_plan_list,
                    'report_actual_list': report_actual_list,
                    }
            )
    else:
        form = ReportDateSelectForm()
    return render_to_response(
        'admin/company_report.html',
        {
            'form': form,
        }
    )