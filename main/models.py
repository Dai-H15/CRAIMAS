from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator


class Companies(models.Model):
    by_U_ID = models.CharField(max_length=100, default="default")
    name = models.CharField(max_length=200, verbose_name='企業・団体名')
    industry = models.CharField(max_length=300, verbose_name='所属業界')
    president = models.CharField(max_length=200, verbose_name='代表者名')
    contact = models.CharField(max_length=200, verbose_name='担当者名')
    Ca_year = models.IntegerField(verbose_name='募集年度')
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
        ("両方", "両方"),
        ("その他", "その他"),
    )
    AboutID = models.CharField(max_length=200, primary_key=True, unique=True)
    by_U_ID = models.CharField(max_length=100, default="default")
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, verbose_name='企業・団体名')
    product = models.TextField(verbose_name='取り扱い製品', blank=True)
    customer_txt = models.TextField(verbose_name='対象顧客', blank=True)
    customer = models.CharField(max_length=50, choices=CHOICES, default="B to B", verbose_name='顧客のタイプ', blank=True)
    value_txt = models.TextField(verbose_name='提供価値の詳細', blank=True)
    value = models.CharField(max_length=50, choices=CHOICES, default="B to B", verbose_name='価値のタイプ', blank=True)
    originality = models.TextField(verbose_name='独自性', blank=True)
    f_value = models.TextField(verbose_name='価値・やりがいを感じるか', blank=True)

    def __str__(self):
        return self.company_name.name + " [About]"

    class Meta:
        verbose_name = '事業内容シート'
        verbose_name_plural = '事業内容シート'


class Idea(models.Model):
    IdeaID = models.CharField(max_length=200, primary_key=True, unique=True)
    by_U_ID = models.CharField(max_length=100, default="default")
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, verbose_name="企業名")
    prospects = models.TextField(verbose_name="今後の事業展開", blank=True)
    valuable = models.TextField(verbose_name="企業が大切にしていること", blank=True)
    statue = models.TextField(verbose_name="企業が求める人物像", blank=True)

    def __str__(self):
        return self.company_name.name + "[Idea]"

    class Meta:
        verbose_name = '経営理念シート'
        verbose_name_plural = '経営理念シート'


class Motivation(models.Model):
    MotivationID = models.CharField(max_length=200, primary_key=True, unique=True)
    by_U_ID = models.CharField(max_length=100, default="default")
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, verbose_name="企業名")
    attraction = models.TextField(verbose_name="企業の魅力", blank=True)
    description = models.TextField(verbose_name="企業の説明", blank=True)
    necessary = models.TextField(verbose_name="求める人物像", blank=True)
    appeal = models.TextField(verbose_name="企業のアピール", blank=True)

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
    founded = models.CharField(max_length=50, verbose_name="設立・創立年", blank=True)
    fonded_t = models.CharField(
        max_length=50, choices=C_Tags["founded_t"], default="null", verbose_name="設立・創立年タグ"
    )

    capital = models.IntegerField(verbose_name="資本金", default=0)
    sales_n = models.IntegerField(verbose_name="売上高", default=0)
    sales_y = models.IntegerField(verbose_name="実績年度", default=0)
    sales_t = models.CharField(max_length=50, choices=C_Tags["sales_t"], default="None", verbose_name="売上高タグ")

    employee_n = models.IntegerField(verbose_name="従業員数", default=0)
    employee_t = models.CharField(
        max_length=50, choices=C_Tags["employee_t"], default="None", verbose_name="従業員数タグ"
    )
    location = models.CharField(max_length=200, verbose_name="所在地", blank=True)
    postal_code = models.CharField(max_length=200, verbose_name="郵便番号", blank=True)
    corporate_number = models.CharField(max_length=20, verbose_name="法人番号", blank=True)
    url = models.CharField(max_length=200, verbose_name="URL", blank=True)
    stock_t = models.CharField(max_length=50, choices=C_Tags["stock_t"], default="None", verbose_name="株式タグ")
    t_p = models.IntegerField(verbose_name="離職率", default=0)
    avg_y = models.IntegerField(verbose_name="平均年齢", default=0)

    def __str__(self):
        return self.company_name.name + "[D_Company]"

    class Meta:
        verbose_name = '企業データシート'
        verbose_name_plural = '企業データシート'


class Adoption(models.Model):
    AdoptionID = models.CharField(max_length=200, primary_key=True, unique=True)
    by_U_ID = models.CharField(max_length=100, default="default")
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, verbose_name="企業名")
    occupation = models.CharField(max_length=200, verbose_name="採用職種", blank=True)
    place = models.CharField(max_length=200, verbose_name="勤務予定地", blank=True)
    n_adopters = models.IntegerField(verbose_name="採用予定人数", default=0)
    n_enrollment = models.IntegerField(verbose_name="OB・OG在籍数", default=0)
    from_url = models.URLField(verbose_name="採用情報URL", blank=True)
    a_year = models.IntegerField(verbose_name="募集年度", default=0)
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
        ("インターンシップ面談", "インターンシップ面談"),
        ("座談会", "座談会"),
        ("エンジニア面接", "エンジニア面接"),
        ("グループディスカッション", "グループディスカッション"),
        ("勉強会／ビジネス体験", "勉強会／ビジネス体験"),
        ("内定", "内定"),
        ("試験", "試験"),
        ("その他", "その他"),
        ("is_Planned", "[特殊設定] テスト等終日利用不可"),
        
    )
    RegistID = models.ForeignKey(RegistSets, on_delete=models.CASCADE)
    InterviewID = models.CharField(max_length=128)
    by_U_ID = models.CharField(max_length=100, default="default")
    company_name = models.CharField(max_length=200, verbose_name="企業名")
    title = models.CharField(max_length=200, verbose_name="面談録タイトル", blank=False)
    tag = models.CharField(max_length=50, choices=tags, default="briefing", verbose_name="タグ")
    date = models.DateTimeField(verbose_name="面談日時", default=timezone.now().strftime('%Y-%m-%d %H:%M'))
    interviewer = models.CharField(max_length=200, verbose_name="面接官名")
    zipcode = models.CharField(max_length=8, verbose_name="郵便番号", blank=True)
    place = models.CharField(max_length=200, verbose_name="面接住所", blank=True)
    Event_URL = models.URLField(verbose_name="イベントURL", blank=True, validators=[URLValidator])
    aspire = models.IntegerField(default=0, verbose_name="志望度(0~100)%")
    reason = models.TextField(default="", verbose_name="志望理由", blank=True)
    want_to = models.TextField(default="", verbose_name="やりたいこと", blank=True)
    note = models.TextField(default="", verbose_name="面談メモ", blank=True)
    review = models.TextField(default="", verbose_name="面談感想", blank=True)

    def __str__(self):
        return self.title + " [Interview]"

    class Meta:
        verbose_name = '面談録シート'
        verbose_name_plural = '面談録シート'


class Interviewer(models.Model):
    by_U_ID = models.CharField(max_length=100, default="default", blank=False)
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE, verbose_name="企業名", blank=False)
    name = models.CharField(max_length=200, verbose_name="面接官名", blank=True)
    position = models.CharField(max_length=200, verbose_name="役職・所属部署等")
    mail = models.EmailField(max_length=200, verbose_name="メールアドレス", blank=True)
    phone = models.CharField(max_length=200, verbose_name="電話番号", blank=True)
    prof_url = models.URLField(verbose_name="プロフィールへのURL", blank=True)
    chance = models.CharField(max_length=200, verbose_name="きっかけ", blank=True)
    introduction = models.TextField(verbose_name="自己紹介", blank=True)
    memo = models.TextField(verbose_name="メモ", blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name="作成日時")

    def __str__(self):
        return self.name + "[Interviewer]"

    class Meta:
        verbose_name = '面接官シート'
        verbose_name_plural = '面接官シート'
