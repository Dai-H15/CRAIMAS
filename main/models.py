from django.db import models


class Companies(models.Model):
    by_U_ID = models.CharField(max_length=100, default="default")
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
    by_U_ID = models.CharField(max_length=100, default="default")
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, verbose_name='企業・団体名')
    product = models.TextField(verbose_name='取り扱い製品')
    customer_txt = models.TextField(verbose_name='対象顧客')
    customer = models.CharField(max_length=50, choices=CHOICES, default="B to B", verbose_name='顧客のタイプ')
    value_txt = models.TextField(verbose_name='提供価値の詳細')
    value = models.CharField(max_length=50, choices=CHOICES, default="B to B", verbose_name='価値のタイプ')
    originality = models.TextField(verbose_name='独自性')
    f_value = models.TextField(verbose_name='価値・やりがいを感じるか')

    def __str__(self):
        return self.company_name.name + " [About]"
    class Meta:
        verbose_name = '事業内容シート'
        verbose_name_plural = '事業内容シート'


class Idea(models.Model):
    IdeaID = models.CharField(max_length=200, primary_key=True, unique=True)
    by_U_ID = models.CharField(max_length=100, default="default")
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, verbose_name="企業名")
    prospects = models.TextField(verbose_name="今後の事業展開")
    valuable = models.TextField(verbose_name="企業が大切にしていること")
    statue = models.TextField(verbose_name="企業が求める人物像")

    def __str__(self):
        return self.company_name.name + "[Idea]"
    class Meta:
        verbose_name = '経営理念シート'
        verbose_name_plural = '経営理念シート'


class Motivation(models.Model):
    MotivationID = models.CharField(max_length=200, primary_key=True, unique=True)
    by_U_ID = models.CharField(max_length=100, default="default")
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, verbose_name="企業名")
    attraction = models.TextField(verbose_name="企業の魅力")
    description = models.TextField(verbose_name="企業の説明")
    necessary = models.TextField(verbose_name="求める人物像")
    appeal = models.TextField(verbose_name="企業のアピール")

    def __str__(self):
        return self.company_name.name + "[Motivation]"
    class Meta:
        verbose_name = '志望動機シート'
        verbose_name_plural = '志望動機シート'


class D_Company(models.Model):
    D_CompanyID = models.CharField(max_length=200, primary_key=True, unique=True)
    by_U_ID = models.CharField(max_length=100, default="default")
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, verbose_name="企業名")
    C_Tags = {
        "founded_t": (
            ("創立100年以上", "創立100年以上"),
            ("創立30以上", "創立30以上"),
            ("なし", "なし"),
        ),
        "sales_t": (
            ("連続増益", "連続増益"),
            ("急増益", "急増益"),
            ("なし", "なし"),
        ),
        "employee_t": (
            ("500名以上", "500名以上"),
            ("400~100名", "400~100名"),
            ("100~20名", "100~20名"),
            ("20名以下", "20名以下"),
            ("なし", "なし"),
        ),
        "stock_t": (
            ("東証一部/二部", "東証一部/二部"),
            ("マザーズ/JASDAQ", "マザーズ/JASDAQ"),
            ("名古屋・札幌・福岡", "名古屋・札幌・福岡"),
            ("なし", "なし"),
        ),
    }
    founded = models.CharField(max_length=50, verbose_name="設立・創立年")
    fonded_t = models.CharField(
        max_length=50, choices=C_Tags["founded_t"], default="null", verbose_name="設立・創立年タグ"
    )

    capital = models.IntegerField(verbose_name="資本金")
    sales_n = models.IntegerField(verbose_name="売上高")
    sales_y = models.IntegerField(verbose_name="実績年度")
    sales_t = models.CharField(max_length=50, choices=C_Tags["sales_t"], default="None", verbose_name="売上高タグ")

    employee_n = models.IntegerField(verbose_name="従業員数")
    employee_t = models.CharField(
        max_length=50, choices=C_Tags["employee_t"], default="None", verbose_name="従業員数タグ"
    )
    location = models.CharField(max_length=200, verbose_name="所在地")
    postal_code = models.CharField(max_length=200, verbose_name="郵便番号")
    corporate_number = models.CharField(max_length=20, verbose_name="法人番号")
    url = models.CharField(max_length=200, verbose_name="URL")
    stock_t = models.CharField(max_length=50, choices=C_Tags["stock_t"], default="None", verbose_name="株式タグ")
    t_p = models.IntegerField(verbose_name="離職率")
    avg_y = models.IntegerField(verbose_name="平均年齢")

    def __str__(self):
        return self.company_name.name + "[D_Company]"

    class Meta:
        verbose_name = '企業データシート'
        verbose_name_plural = '企業データシート'


class Adoption(models.Model):
    AdoptionID = models.CharField(max_length=200, primary_key=True, unique=True)
    by_U_ID = models.CharField(max_length=100, default="default")
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, verbose_name="企業名")
    occupation = models.CharField(max_length=200, verbose_name="採用職種")
    place = models.CharField(max_length=200, verbose_name="勤務予定地")
    n_adopters = models.IntegerField(verbose_name="採用予定人数")
    n_enrollment = models.IntegerField(verbose_name="OB・OG在籍数")
    a_year = models.IntegerField(verbose_name="募集年度")
    created = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

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

    class Meta:
        verbose_name = '登録情報シート'
        verbose_name_plural = '登録情報シート'


class Interview(models.Model):
    tags = (
        ("説明会", "説明会"),
        ("カジュアル面接", "カジュアル面接"),
        ("一次面接", "一次面接"),
        ("二次面接", "二次面接"),
        ("三次面接", "三次面接"),
        ("最終面接", "最終面接"),
        ("インターンシップ", "インターンシップ"),
        ("インターンシップ説明会", "インターンシップ説明会"),
        ("座談会", "座談会"),
        ("エンジニア面接", "エンジニア面接"),
        ("グループディスカッション", "グループディスカッション"),
        ("勉強会／ビジネス体験", "勉強会／ビジネス体験"),
        ("内定", "内定"),
        ("試験", "試験"),
        ("その他", "その他")
    )
    RegistID = models.ForeignKey(RegistSets, on_delete=models.CASCADE)
    InterviewID = models.CharField(max_length=128)
    by_U_ID = models.CharField(max_length=100, default="default")
    company_name = models.CharField(max_length=200, verbose_name="企業名")
    title = models.CharField(max_length=200, verbose_name="面談録タイトル")
    tag = models.CharField(max_length=50, choices=tags, default="briefing", verbose_name="タグ")
    date = models.DateTimeField(verbose_name="面談日時")
    interviewer = models.CharField(max_length=200, verbose_name="面接官名")
    zipcode = models.CharField(max_length=8, verbose_name="郵便番号")
    place = models.CharField(max_length=200, verbose_name="面接住所")
    aspire = models.IntegerField(default=0, verbose_name="志望度(0~100)%")
    reason = models.TextField(default="", verbose_name="志望理由")
    want_to = models.TextField(default="", verbose_name="やりたいこと")
    note = models.TextField(default="", verbose_name="面談メモ")
    review = models.TextField(default="", verbose_name="面談感想")

    def __str__(self):
        return self.title + " [Interview]"

    class Meta:
        verbose_name = '面談録シート'
        verbose_name_plural = '面談録シート'


class Interviewer(models.Model):
    by_U_ID = models.CharField(max_length=100, default="default")
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, verbose_name="企業名", blank=True)
    name = models.CharField(max_length=200, verbose_name="面接官名", blank=True)
    position = models.CharField(max_length=200, verbose_name="役職")
    mail = models.EmailField(max_length=200, verbose_name="メールアドレス", blank=False)
    phone = models.CharField(max_length=200, verbose_name="電話番号", blank=False)
    introduction = models.TextField(verbose_name="自己紹介")
    memo = models.TextField(verbose_name="メモ")
    created = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    def __str__(self):
        return self.name + "[Interviewer]"

    class Meta:
        verbose_name = '面接官シート'
        verbose_name_plural = '面接官シート'
