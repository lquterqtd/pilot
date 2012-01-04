#coding:utf-8
from django.db import models
import datetime
# Create your models here.
MAX_CONTRACT_ID_LENGTH = 11
########################################################################
CONTRACT_STATUS = (
    ('ZC', '正常'),
    ('JS', '结束'),
    ('QT', '其它'),
    )
class SelfFeeContractInfo(models.Model):
    """"""
    contract_id = models.CharField('合同号', max_length=MAX_CONTRACT_ID_LENGTH, unique=True)
    contract_amount = models.FloatField('合同金额(万)', blank=True, null=True)
    contract_status = models.CharField('合同状态', max_length=2, choices=CONTRACT_STATUS)
    available_hours = models.CharField('可飞小时数', max_length=20, blank=True)
    actual_hours = models.CharField('实飞小时数', max_length=20, blank=True)
    class Meta:
        verbose_name = '自费合同信息'
        verbose_name_plural = '自费合同信息'
    #----------------------------------------------------------------------
    def get_student_name(self):
        """"""
        try:
            p = SelfFeeStudent.objects.get(contract_id=self.contract_id)
        except SelfFeeStudent.DoesNotExist:
            return u'没有找到该合同对应的学员'
        else:
            return p.name
    get_student_name.short_description = '姓名'
    #----------------------------------------------------------------------
    def get_contract_amount(self):
        """"""
        if not self.contract_amount:
            return u''
        else:
            return self.contract_amount
    get_contract_amount.short_description = '合同金额(万)'
    #----------------------------------------------------------------------
    def get_arrears_info(self):
        """"""
        p = ReceivablesInfo.objects.filter(contract=self.pk)
        if p.count() == 0:
            return u''
        sum_arrears = 0
        for receivablesinfo in p:
            if receivablesinfo.actual_amount != None and receivablesinfo.plan_amount != None and receivablesinfo.actual_amount < receivablesinfo.plan_amount:
                sum_arrears += receivablesinfo.plan_amount - receivablesinfo.actual_amount
        if sum_arrears == 0:
            return u''
        else:
            return u'<font color="#dd0000">%d</font>' % sum_arrears
    get_arrears_info.allow_tags = True
    get_arrears_info.short_description = '欠款(元)'
    def __unicode__(self):
        return self.contract_id
########################################################################
class CompanyInfo(models.Model):
    """"""
    company_name = models.CharField('所属单位', max_length=30)
    class Meta:
        verbose_name = '所属单位'
        verbose_name_plural = '所属单位'
    def __unicode__(self):
        return self.company_name
########################################################################
class CompanySponsoredContractInfo(models.Model):
    """"""
    company = models.ForeignKey(CompanyInfo)
    contract_id =  models.CharField('合同号', max_length=MAX_CONTRACT_ID_LENGTH)
    contract_amount = models.FloatField('合同金额(万)', blank=True, null=True)
    remarks = models.TextField('备注', blank=True)
    class Meta:
        verbose_name = '公司委培合同'
        verbose_name_plural = '公司委培合同'
    def __unicode__(self):
        return self.contract_id
    #----------------------------------------------------------------------
    def get_company_name(self):
        """"""
        try:
            p = CompanyInfo.objects.get(pk=self.company_id)
        except CompanyInfo.DoesNotExist:
            return u'没有找到该合同所属的公司'
        else:
            return p.company_name
    get_company_name.short_description = '所属单位'
    #----------------------------------------------------------------------
    def get_arrears_info(self):
        """"""
        p = SponsoredReceivablesInfo.objects.filter(contract=self.pk)
        if p.count() == 0:
            return u''
        sum_arrears = 0
        for receivablesinfo in p:
            if receivablesinfo.actual_amount != None and receivablesinfo.plan_amount != None and receivablesinfo.actual_amount < receivablesinfo.plan_amount:
                sum_arrears += receivablesinfo.plan_amount - receivablesinfo.actual_amount
        if sum_arrears == 0:
            return u''
        else:
            return u'<font color="#dd0000">%d</font>' % sum_arrears
    get_arrears_info.allow_tags = True
    get_arrears_info.short_description = '欠款(元)'
    #----------------------------------------------------------------------
    def get_students_count(self):
        """"""
        p = SelfFeeStudent.objects.filter(contract_id=self.contract_id)
        if p.count() == 0:
            return u'0'
        else:
            return u'<a href="/admin/info/selffeestudent/?contract_id__exact=%s">%d</a>' % (self.contract_id, p.count())

    get_students_count.allow_tags = True
    get_students_count.short_description = '人数'
    #----------------------------------------------------------------------
    def get_contract_amount(self):
        """"""
        if not self.contract_amount:
            return u''
        else:
            return self.contract_amount
    get_contract_amount.short_description = '合同金额(万)'
    #----------------------------------------------------------------------
    def get_executed_info(self):
        """"""
        try:
            p = ContractExecutedInfo.objects.get(contract_id=self.contract_id)
        except ContractExecutedInfo.DoesNotExist:
            create_contract = ContractExecutedInfo(
                contract_id=self.contract_id,
                company=self.company,
                contract_cycle=0
            )
            create_contract.save()
            return u'<a href="/admin/info/contractexecutedinfo/%d/">查看</a>' % create_contract.pk
        else:
            return u'<a href="/admin/info/contractexecutedinfo/%d/">查看</a>' % p.pk
    get_executed_info.allow_tags = True
    get_executed_info.short_description = '合同执行信息'
EDUCATION_CHOICE = (
    ('GZ', '高中'),
    ('DZ', '大专'),
    ('BK', '本科'),
    ('SS', '硕士'),
    ('QT', '其它'),
)
STUDENT_TYPE = (
    ('ZF', '自费'),
    ('JTNWP', '集团内委培'),
    ('WPJY', '委培教员'),
    ('JTWWP', '集团外委培'),
    ('HZ', '换照'),
    ('BCXL', '补充训练'),
    ('QT', '其它'),
)
STUDENT_STATUS = (
    ('ZX', '在校'),
    ('TF', '停飞'),
    ('TX', '退学'),
    ('BYLX', '毕业离校'),
    ('QT', '其它'),
)
TRAINING_PHASE = (
    ('LL', '理论'),
    ('FX', '飞行'),
    ('QT', '其它'),
)
SCHOOL_TIME_YEAR = (
    ('2010', '2010年'),
    ('2011', '2011年'),
    ('2012', '2012年'),
    ('2013', '2013年'),
    ('2014', '2014年'),
)
SCHOOL_TIME_MONTH = (
    ('1', '1月'),
    ('2', '2月'),
    ('3', '3月'),
    ('4', '4月'),
    ('5', '5月'),
    ('6', '6月'),
    ('7', '7月'),
    ('8', '8月'),
    ('9', '9月'),
    ('10', '10月'),
    ('11', '11月'),
    ('12', '12月'),
)
########################################################################
class SelfFeeStudent(models.Model):
    """"""
    student_number = models.CharField('学号', max_length=7, unique=True, help_text='学号为7位长度')
    name = models.CharField('姓名', max_length=10)
    gender = models.CharField('性别', max_length=1, choices=(('M', '男'), ('F', '女')))
    id_number = models.CharField('身份证号码', max_length=18, blank=True)
    tel = models.CharField('电话', max_length=15, blank=True)
    graduated_from = models.CharField('毕业院校', max_length=30, blank=True)
    education = models.CharField('学历', max_length=10, choices=EDUCATION_CHOICE)
    school_time_year = models.CharField('入校年份', max_length=4, choices=SCHOOL_TIME_YEAR)
    school_time_month = models.CharField('入校月份', max_length=2, choices=SCHOOL_TIME_MONTH)
    student_type = models.CharField('类别', max_length=5, choices=STUDENT_TYPE)
    company = models.ForeignKey(
        to=CompanyInfo,
        to_field='id',
        verbose_name='单位',
        help_text='若下拉菜单中没有该单位，则需点击右侧的"+"号添加'
    )
    grade = models.CharField('班期', max_length=5, blank=True)
    remarks = models.TextField('备注', blank=True)
    contract_id = models.CharField('合同号', max_length=MAX_CONTRACT_ID_LENGTH, blank=True)
    training_outline = models.CharField('培训大纲', max_length=20, blank=True)
    student_status = models.CharField('学员状态', max_length=4, choices=STUDENT_STATUS)
    training_phase = models.CharField('培训阶段', max_length=4, choices=TRAINING_PHASE, help_text="如果学员已毕业离校请选择'其它'")
    actual_hours = models.CharField('实飞小时数', max_length=20, blank=True, default='::', help_text='填写格式为"小时:分钟:秒",如"123:45:6"')
    commercial_license = models.BooleanField(
        '商照结束',
        default=False,
        help_text='默认未勾选即表示未结束，选中则表示商照结束'
    )
    class Meta:
        verbose_name = '学员基本信息'
        verbose_name_plural = '学员基本信息'
    def __unicode__(self):
        return self.name
    #----------------------------------------------------------------------
    def get_school_time(self):
        """"""
        return u'%s年%s月' % (self.school_time_year, self.school_time_month)
    get_school_time.short_description = '入校时间'
    #----------------------------------------------------------------------
    def contract_id_link(self):
        """"""
        if self.contract_id != None and len(self.contract_id) > 0:
            if self.student_type == 'ZF':
                try:
                    p = SelfFeeContractInfo.objects.get(contract_id=self.contract_id)
                except SelfFeeContractInfo.DoesNotExist:
                    create_contract = SelfFeeContractInfo(
                        contract_id=self.contract_id,
                        contract_status='ZC'
                    )
                    create_contract.save()
                    return u'<a href="/admin/info/selffeecontractinfo/%d/">%s</a>' % (create_contract.pk, self.contract_id)
                else:
                    return u'<a href="/admin/info/selffeecontractinfo/%d/">%s</a>' % (p.pk, self.contract_id)
            elif self.student_type == 'JTNWP':
                try:
                    p = CompanySponsoredContractInfo.objects.get(contract_id=self.contract_id)
                except CompanySponsoredContractInfo.DoesNotExist:
                    create_contract = CompanySponsoredContractInfo(
                        contract_id=self.contract_id,
                        company_id=self.company_id
                    )
                    create_contract.save()
                    return u'<a href="/admin/info/companysponsoredcontractinfo/%d/">%s</a>' % (create_contract.pk, self.contract_id)
                else:
                    return u'<a href="/admin/info/companysponsoredcontractinfo/%d/">%s</a>' % (p.pk, self.contract_id)
            else:
                return self.contract_id
        else:
            return u'未填写'
    contract_id_link.allow_tags = True
    contract_id_link.short_description = '合同号'

########################################################################
class ReceivablesInfo(models.Model):
    """"""
    contract = models.ForeignKey(SelfFeeContractInfo)
    time_node = models.CharField('时间节点', max_length=30, blank=True)
    plan_amount = models.FloatField('应收金额(元)', blank=True, null=True)
    plan_date = models.DateField('应收款日期', blank=True, null=True)
    actual_amount = models.FloatField('实收金额(元)', blank=True, null=True)
    actual_date = models.DateField('实收款日期', blank=True, null=True)
    class Meta:
        verbose_name = '自费收款信息'
        verbose_name_plural = '自费收款信息'
    def __unicode__(self):
        return u'收款信息'
########################################################################
class SponsoredReceivablesInfo(models.Model):
    """"""
    contract = models.ForeignKey(CompanySponsoredContractInfo)
    time_node = models.CharField('时间节点', max_length=30, blank=True)
    plan_amount = models.FloatField('应收金额(万)', blank=True, null=True)
    plan_date = models.DateField('应收款日期', blank=True, null=True)
    actual_amount = models.FloatField('实收金额(万)', blank=True, null=True)
    actual_date = models.DateField('实收款日期', blank=True, null=True)
    class Meta:
        verbose_name = '委培合同收款信息'
        verbose_name_plural = '委培合同收款信息'
    def __unicode__(self):
        return u''
########################################################################
class ContractExecutedInfo(models.Model):
    """"""
    company = models.ForeignKey(CompanyInfo)
    contract_id = models.CharField('合同号', max_length=MAX_CONTRACT_ID_LENGTH, blank=True)
    contract_cycle = models.IntegerField('合同周期(月)')
    theory_plan_time_start = models.DateField('理论计划开始时间', blank=True, null=True)
    theory_plan_time_end = models.DateField('理论计划结束时间', blank=True, null=True)
    theory_actual_time_start = models.DateField('理论实际开始时间', blank=True, null=True)
    theory_actual_time_end = models.DateField('理论实际结束时间', blank=True, null=True)
    flight_plan_time_start = models.DateField('飞行计划开始时间', blank=True, null=True)
    flight_plan_time_end = models.DateField('飞行计划结束时间', blank=True, null=True)
    flight_actual_time_start = models.DateField('飞行实际开始时间', blank=True, null=True)
    flight_actual_time_end = models.DateField('飞行实际结束时间', blank=True, null=True)
    remarks = models.TextField('备注', blank=True)
    class Meta:
        verbose_name = '合同执行时间'
        verbose_name_plural = '合同执行时间'
    def __unicode__(self):
        return self.contract_id
    def get_company_name(self):
        try:
            p = CompanyInfo.objects.get(pk=self.company_id)
        except CompanyInfo.DoesNotExist:
            return u'不存在'
        else:
            return p.company_name
    get_company_name.short_description = '单位名称'
    #----------------------------------------------------------------------
    def theory_date(self):
        """"""
        str = u'计划时间:'
        if self.theory_plan_time_start == None and self.theory_plan_time_end == None:
            str += u'/<br>'
        else:
            t = u'%s至%s<br>' % (self.theory_plan_time_start, self.theory_plan_time_end)
            str += t
        str += u'实际时间:'
        if self.theory_actual_time_start == None and self.theory_actual_time_end == None:
            str += u'/<br>'
        else:
            t = u'%s至%s<br>' % (self.theory_actual_time_start, self.theory_actual_time_end)
            str += t
        return str
    theory_date.allow_tags = True
    theory_date.short_description = '理论'
    #----------------------------------------------------------------------
    def flight_date(self):
        """"""
        str = u'计划时间:'
        if self.flight_plan_time_start == None and self.flight_plan_time_end == None:
            str += u'/<br>'
        else:
            t = u'%s至%s<br>' % (self.flight_plan_time_start, self.flight_plan_time_end)
            str += t
        str += u'实际时间:'
        if self.flight_actual_time_start == None and self.flight_actual_time_end == None:
            str += u'/<br>'
        else:
            t = u'%s至%s<br>' % (self.flight_actual_time_start, self.flight_actual_time_end)
            str += t
        return str
    flight_date.allow_tags = True
    flight_date.short_description = '飞行'
    #----------------------------------------------------------------------
    def is_in(self, a, b, c, aa, bb, cc, y, m, d):
        """"""
        if y >= a and y <= aa and m >= b and m <= bb and d >=c and d <= cc:
            return True
        else:
            return False
    #----------------------------------------------------------------------
    def is_overdue(self):
        """"""
        y = datetime.datetime.now().year
        m = datetime.datetime.now().month
        d = datetime.datetime.now().day
        res = u''
        if self.theory_plan_time_start != None:
            if not self.is_in(
                self.theory_plan_time_start.year,
                self.theory_plan_time_start.month,
                self.theory_plan_time_start.day,
                self.theory_plan_time_end.year,
                self.theory_plan_time_end.month,
                self.theory_plan_time_end.day,
                y, m, d
            ):
                res += u'<font color="#dd0000">理论时间超期</font><br>'
        if self.flight_plan_time_start != None:
            if not self.is_in(
                self.flight_plan_time_start.year,
                self.flight_plan_time_start.month,
                self.flight_plan_time_start.day,
                self.flight_plan_time_end.year,
                self.flight_plan_time_end.month,
                self.flight_plan_time_end.day,
                y, m, d
            ):
                res += u'<font color="#dd0000">飞行时间超期</font><br>'
        return res
    is_overdue.allow_tags = True
    is_overdue.short_description = '是否超期'