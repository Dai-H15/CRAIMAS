from django import forms
from .models import Companies, About, Idea, Motivation, D_Company, Adoption, Interview, RegistSets, Interviewer


class CompaniesForm(forms.ModelForm):
    class Meta:
        model = Companies
        fields = ("name", "industry", "president", "contact", "Ca_year")
        labels = {
            "name": "企業・団体名",
            "industry": "所属業界",
            "president": "代表者",
            "contact": "担当者",
            "Ca_year": "募集年度"
        }


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ("product", "customer_txt", "customer", "value_txt", "value", "originality", "f_value")
        labels = {
            "product": "取り扱い製品",
            "customer_txt": "対象顧客",
            "customer": "顧客のタイプ",
            "value_txt": "提供価値の詳細",
            "value": "価値のタイプ",
            "originality": "独自性",
            "f_value": "価値・やりがいを感じるか"
        }


class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ("prospects", "valuable", "statue")
        labels = {
            "prospects": "今後の事業展開",
            "valuable": "企業が大切にしていること",
            "statue": "企業が求める人物像"
        }


class MotivationForm(forms.ModelForm):
    class Meta:
        model = Motivation
        fields = ("attraction", "description", "necessary", "appeal")
        labels = {
            "attraction": "企業の魅力",
            "description": "企業の説明",
            "necessary": "求める人物像",
            "appeal": "企業のアピール"
        }


class D_CompanyForm(forms.ModelForm):
    class Meta:
        model = D_Company
        fields = ("founded", "fonded_t", "capital", "sales_n", "sales_y", "sales_t", "employee_n", "employee_t", "stock_t", "t_p", "avg_y", "postal_code", "location", "corporate_number", "url")
        labels = {
            "founded": "設立・創立年",
            "fonded_t": "設立・創立年タグ",
            "capital": "資本金",
            "sales_n": "売上高",
            "sales_y": "実績年度",
            "sales_t": "売上高タグ",
            "employee_n": "従業員数",
            "employee_t": "従業員数タグ",
            "stock_t": "株式タグ",
            "t_p": "離職率",
            "avg_y": "平均年齢",
            "postal_code": "郵便番号",
            "location": "所在地",
            "corporate_number": "法人番号",
            "url": "URL",
        }


class AdoptionForm(forms.ModelForm):
    class Meta:
        model = Adoption
        fields = ("occupation", "place", "n_adopters", "n_enrollment", "from_url", "a_year")
        labels = {
            "occupation": "採用職種",
            "place": "勤務予定地",
            "n_adopters": "採用予定人数",
            "n_enrollment": "OB・OG在籍数",
            "from_url": "採用情報URL",
            "a_year": "募集年度",
        }


class SearchForm_corpnum(forms.Form):
    pref_choice = (
        ("00", "---"),
        ("01", '北海道'),
        ("02", '青森県'),
        ("03", '岩手県'),
        ("04", '宮城県'),
        ("05", '秋田県'),
        ("06", '山形県'),
        ("07", '福島県'),
        ("08", '茨城県'),
        ("09", '栃木県'),
        (10, '群馬県'),
        (11, '埼玉県'),
        (12, '千葉県'),
        (13, '東京都'),
        (14, '神奈川県'),
        (15, '新潟県'),
        (16, '富山県'),
        (17, '石川県'),
        (18, '福井県'),
        (19, '山梨県'),
        (20, '長野県'),
        (21, '岐阜県'),
        (22, '静岡県'),
        (23, '愛知県'),
        (24, '三重県'),
        (25, '滋賀県'),
        (26, '京都府'),
        (27, '大阪府'),
        (28, '兵庫県'),
        (29, '奈良県'),
        (30, '和歌山県'),
        (31, '鳥取県'),
        (32, '島根県'),
        (33, '岡山県'),
        (34, '広島県'),
        (35, '山口県'),
        (36, '徳島県'),
        (37, '香川県'),
        (38, '愛媛県'),
        (39, '高知県'),
        (40, '福岡県'),
        (41, '佐賀県'),
        (42, '長崎県'),
        (43, '熊本県'),
        (44, '大分県'),
        (45, '宮崎県'),
        (46, '鹿児島県'),
        (47, '沖縄県')
    )
    name = forms.CharField(label="企業名", required=False)
    corporate_number = forms.CharField(label="法人番号", required=False)
    prefecture = forms.ChoiceField(label="都道府県", choices=pref_choice, required=False)


class InterviewForm(forms.ModelForm):
    RegistID = forms.ModelChoiceField(queryset=RegistSets.objects.all(), to_field_name="RegistID", widget=forms.HiddenInput())

    class Meta:
        model = Interview
        fields = ("RegistID", "InterviewID", "title", "tag", "date", "interviewer", "zipcode", "place", "aspire", "reason", "want_to", "note", "review")
        labels = {
                    "RegistID": "登録セットキー",
                    "InterviewID": "インタビューキー",
                    "title": "面談タイトル",
                    "tag": "面談タグ",
                    "date": "面談日時",
                    "interviewer": "面談者",
                    "zipcode": "郵便番号",
                    "place": "住所",
                    "aspire": "志望度(0~100)%",
                    "reason": "志望理由",
                    "want_to": "やりたいこと",
                    "notes": "面談メモ",
                    "review": "面談感想"
                  }
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "aspire": forms.NumberInput(attrs={ "min": "0", "max": "100", "step": "1"}),
            "InterviewID": forms.HiddenInput()

        }


class Form_Prof_Interviewer(forms.ModelForm):
    class Meta:
        model = Interviewer
        fields = ("position", "mail", "phone", "prof_url", "chance", "introduction", "memo")
        labels = {
            "position": "役職・所属部署等",
            "mail": "メールアドレス",
            "phone": "電話番号",
            "prof_url": "プロフィールへのURL",
            "chance": "知ったきっかけ",
            "introduction": "自己紹介",
            "memo": "メモ"
        }