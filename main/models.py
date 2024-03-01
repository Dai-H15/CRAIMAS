from django.db import models


class Companies(models.Model):
    name = models.CharField(max_length=200)
    industry = models.CharField(max_length=200)
    president = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    a_year = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name


class About(models.Model):
    CHOICES = (
        ("B to B", "B to B"),
        ("B to C", "B to C"),
    )
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE)
    product = models.TextField()
    customer_txt = models.TextField()
    customer = models.CharField(max_length=50, choices=CHOICES, default="B to B")
    value_txt = models.TextField()
    value = models.CharField(max_length=50, choices=CHOICES, default="B to B")
    originality = models.TextField()
    f_value = models.TextField()

    def __str__(self):
        return self.company_name.name


class Idea(models.Model):
    company_name = models.ForeignKey(Companies, on_delete=models.CASCADE)
    prospects = models.TextField()
    valuable = models.TextField()
    statue = models.TextField()


class Motivation(models.Model):
    companyame = models.ForeignKey(Companies, on_delete=models.CASCADE)
    attraction = models.TextField()
    description = models.TextField()
    necessary = models.TextField()
    appeal = models.TextField()


class D_Company(models.Model):
    companyame = models.ForeignKey(Companies, on_delete=models.CASCADE)
    C_Tags = {
        "founded_t": (
            ("more100", "創立100年以上"),
            ("more30", "創立30以上"),
            ("null", "なし")
        ),
        "sales_t": (
            ("consecutive", "連続増益"),
            ("sudden", "急増益"),
            ("None", "なし")
        ),
        "employee_t": (
            ("more500", "500名以上"),
            ("400~100", "400~100名"),
            ("100~20", "100~20名"),
            ("less20", "20名以下"),
            ("None", "なし")
        ),
        "stock_t": (
            ("TSE", "東証一部/二部"),
            ("MOJ", "マザーズ/JASDAQ"),
            ("OTH", "名古屋・札幌・福岡"),
            ("None", "なし"),
        )
    }
    founded = models.IntegerField()
    fonded_t = models.CharField(max_length=50, choices=C_Tags["founded_t"], default="null")

    capital = models.IntegerField()
    sales_n = models.IntegerField()
    sales_y = models.IntegerField()
    sales_t = models.CharField(max_length=50, choices=C_Tags["sales_t"], default="None")

    employee_n = models.IntegerField()
    employee_t = models.CharField(max_length=50, choices=C_Tags["employee_t"], default="None")

    stock_t = models.CharField(max_length=50, choices=C_Tags["stock_t"], default="None")
    t_p = models.IntegerField()
    avg_y = models.IntegerField()


class Adoption(models.Model):
    companyame = models.ForeignKey(Companies, on_delete=models.CASCADE)
    occupation = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    n_adopters = models.IntegerField()
    n_enrollment = models.IntegerField()
    a_year = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)


class RegistSets(models.Model):
    by_c_id = models.CharField(max_length=100)
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    about = models.ForeignKey(About, on_delete=models.CASCADE)
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE)
    motivation = models.ForeignKey(Motivation, on_delete=models.CASCADE)
    d_company = models.ForeignKey(D_Company, on_delete=models.CASCADE)
    adoption = models.ForeignKey(Adoption, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    regist_publish = models.BooleanField(default=False)

    def __str__(self):
        return self.company.name
