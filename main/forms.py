from django import forms
from .models import Companies, About, Idea, Motivation, D_Company, Adoption


class CompaniesForm(forms.ModelForm):
    class Meta:
        model = Companies
        fields = ("name", "industry", "president", "contact", "a_year")
        labels = {
            "name": "企業・団体名",
            "industry": "所属業界",
            "president": "代表者名",
            "contact": "担当者名",
            "a_year": "募集年度"
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
        fields = ("founded", "fonded_t", "capital", "sales_n", "sales_y", "sales_t", "employee_n", "employee_t", "stock_t", "t_p", "avg_y")
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
            "avg_y": "平均年齢"
        }


class AdoptionForm(forms.ModelForm):
    class Meta:
        model = Adoption
        fields = ("occupation", "place", "n_adopters", "n_enrollment", "a_year")
        labels = {
            "occupation": "採用職種",
            "place": "勤務予定地",
            "n_adopters": "採用予定人数",
            "n_enrollment": "OB・OG在籍数",
            "a_year": "募集年度",
        }