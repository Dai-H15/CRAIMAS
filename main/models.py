from django.db import models


class Companies(models.Model):
    name = models.CharField(max_length=200, verbose_name='企業・団体名')
    industry = models.CharField(max_length=200, verbose_name='所属業界')
    president = models.CharField(max_length=200, verbose_name='代表者名')
    contact = models.CharField(max_length=200, verbose_name='担当者名')
    a_year = models.IntegerField(verbose_name='募集年度')
    created = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    CompanyID = models.CharField(max_length=200, primary_key=True, unique=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name = '企業シート'
        verbose_name_plural = '企業シート'



class About(models.Model):
    CHOICES = (
        ("B to B", "B to B"),
        ("B to C", "B to C"),
    )
    AboutID = models.CharField(max_length=200, primary_key=True, unique=True)
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE)
    product = models.TextField()
    customer_txt = models.TextField()
    customer = models.CharField(max_length=50, choices=CHOICES, default="B to B")
    value_txt = models.TextField()
    value = models.CharField(max_length=50, choices=CHOICES, default="B to B")
    originality = models.TextField()
    f_value = models.TextField()

    def __str__(self):
        return self.company_name.name + " [About]"
    class Meta:
        verbose_name = '事業内容シート'
        verbose_name_plural = '事業内容シート'


class Idea(models.Model):
    IdeaID = models.CharField(max_length=200, primary_key=True, unique=True)
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE)
    prospects = models.TextField()
    valuable = models.TextField()
    statue = models.TextField()

    def __str__(self):
        return self.company_name.name + "[Idea]"
    class Meta:
        verbose_name = '経営理念シート'
        verbose_name_plural = '経営理念シート'


class Motivation(models.Model):
    MotivationID = models.CharField(max_length=200, primary_key=True, unique=True)
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE)
    attraction = models.TextField()
    description = models.TextField()
    necessary = models.TextField()
    appeal = models.TextField()

    def __str__(self):
        return self.company_name.name + "[Motivation]"
    class Meta:
        verbose_name = '志望動機シート'
        verbose_name_plural = '志望動機シート'


class D_Company(models.Model):
    D_CompanyID = models.CharField(max_length=200, primary_key=True, unique=True)
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE)
    C_Tags = {
        "founded_t": (
            ("more100", "創立100年以上"),
            ("more30", "創立30以上"),
            ("null", "なし"),
        ),
        "sales_t": (
            ("consecutive", "連続増益"),
            ("sudden", "急増益"),
            ("None", "なし"),
        ),
        "employee_t": (
            ("more500", "500名以上"),
            ("400~100", "400~100名"),
            ("100~20", "100~20名"),
            ("less20", "20名以下"),
            ("None", "なし"),
        ),
        "stock_t": (
            ("TSE", "東証一部/二部"),
            ("MOJ", "マザーズ/JASDAQ"),
            ("OTH", "名古屋・札幌・福岡"),
            ("None", "なし"),
        ),
    }
    founded = models.CharField(max_length=50)
    fonded_t = models.CharField(
        max_length=50, choices=C_Tags["founded_t"], default="null"
    )

    capital = models.IntegerField()
    sales_n = models.IntegerField()
    sales_y = models.IntegerField()
    sales_t = models.CharField(max_length=50, choices=C_Tags["sales_t"], default="None")

    employee_n = models.IntegerField()
    employee_t = models.CharField(
        max_length=50, choices=C_Tags["employee_t"], default="None"
    )
    location = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=200)
    corporate_number = models.CharField(max_length=20)
    url = models.CharField(max_length=200)
    stock_t = models.CharField(max_length=50, choices=C_Tags["stock_t"], default="None")
    t_p = models.IntegerField()
    avg_y = models.IntegerField()

    def __str__(self):
        return self.company_name.name + "[D_Company]"
    class Meta:
        verbose_name = '企業データシート'
        verbose_name_plural = '企業データシート'


class Adoption(models.Model):
    AdoptionID = models.CharField(max_length=200, primary_key=True, unique=True)
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    n_adopters = models.IntegerField()
    n_enrollment = models.IntegerField()
    a_year = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.company_name.name + "[Adoption]"
    class Meta:
        verbose_name = '採用情報シート'
        verbose_name_plural = '採用情報シート'


class RegistSets(models.Model):
    RegistID = models.CharField(max_length=128, primary_key=True, unique=True)
    by_U_ID = models.CharField(max_length=100)
    company = models.ForeignKey(Companies, on_delete=models.SET_NULL, null=True, blank=True)
    about = models.ForeignKey(About, on_delete=models.SET_NULL, null=True, blank=True)
    idea = models.ForeignKey(Idea, on_delete=models.SET_NULL, null=True, blank=True)
    motivation = models.ForeignKey(Motivation, on_delete=models.SET_NULL, null=True, blank=True)
    d_company = models.ForeignKey(D_Company, on_delete=models.SET_NULL, null=True, blank=True)
    adoption = models.ForeignKey(Adoption, on_delete=models.SET_NULL, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    regist_publish = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        if self.company is not None:
            return self.company.name
        else:
            return 'No Company'


class Interview(models.Model):
    tags = (
        ("briefing", "説明会"),
        ("casual", "カジュアル面接"),
        ("1_interview", "一次面接"),
        ("2_interview", "二次面接"),
        ("3_interview", "三次面接"),
        ("l_interview", "最終面接"),
        ("internship", "インターンシップ"),
        ("engineer", "エンジニア面接"),
        ("group", "グループディスカッション"),
        ("study", "勉強会／ビジネス体験"),
        ("offer", "内定"),
        ("test", "試験"),
        ("other", "その他")
    )
    RegistID = models.ForeignKey(RegistSets, on_delete=models.CASCADE)
    InterviewID = models.CharField(max_length=128)
    company_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=50, choices=tags, default="briefing")
    date = models.DateTimeField()
    interviewer = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=8)
    place = models.CharField(max_length=200)
    aspire = models.IntegerField(default=0)
    reason = models.TextField(default="")
    want_to = models.TextField(default="")
    note = models.TextField(default="")
    review = models.TextField(default="")

    def __str__(self):
        return self.title + " [Interview]"
    class Meta:
        verbose_name = '面談録シート'
        verbose_name_plural = '面談録シート'


class CustomSheet(models.Model):
    sheet_id = models.CharField(max_length=100, primary_key=True, unique=True)
    by_U_ID = models.CharField(max_length=100, default="default")
    sheet_name = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    selected_field = models.JSONField()
    view_settings = models.JSONField()
    search_settings = models.JSONField()

    def __str__(self):
        return self.sheet_name
    class Meta:
        verbose_name = 'カスタムシート'
        verbose_name_plural = 'カスタムシート'
