from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main.views import collect_regnum
from django.shortcuts import redirect, HttpResponse
from main.models import (
    RegistSets,
    Interview,
)

from .models import CustomSheet
from django.core.exceptions import FieldError as Django_FieldError
from django.db.models import Sum, Avg
from django.apps import apps
import secrets
from django.urls import reverse
from django.forms.models import model_to_dict
import json, datetime, urllib


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)


@login_required
def view_index(request):
    contexts = collect_regnum(request)
    return render(request, "view/view_index.html", contexts)


@login_required
def view_main(request, control, option):
    contexts = collect_regnum(request)
    contexts["control"] = control

    ForeignKeySets = {
        "company_name": "company_name__name"
    }
    menu = [
        {"choice": "top", "desc": "トップページ", "th_all": []},
        {
            "choice": "all",
            "desc": "全企業シート一覧",
            "th_all": {
                "company": "企業名",
                "company.industry": "所属業界",
                "adoption.occupation": "採用職種",
                "d_company.url": "URL",
                "created": "登録日",
                "": "詳細",
            },
        },
        {
            "choice": "interview",
            "desc": "面談録一覧",
            "th_all": ["企業名", "面談名", "面談日", "志望度(%)", "詳細"],
        },
        {
            "choice": "cat_interview",
            "desc": "カテゴリ別面談録",
            "th_all": ["企業名", "面談名", "面談日", "担当者", "志望度(%)",  "詳細"],
        },
        {
            "choice": "R_aspire",
            "desc": "志望度ランキング",
            "th_all": ["企業名", "面談回数", "志望度合計", "平均志望度", "詳細"],
        },
    ]
    if CustomSheet.objects.filter(by_U_ID=request.user.U_ID).count() > 0:
        for cs in CustomSheet.objects.filter(by_U_ID=request.user.U_ID):
            menu.append({"choice": cs.sheet_name, "desc": cs.sheet_name, "th_all": []})
    for m in menu:
        if m["choice"] == control:
            current_menu = m
            m["current"] = "true"
            m["active"] = "active"
        else:
            m["current"] = "false"
            m["active"] = ""

    if control == "all":
        results = RegistSets.objects.filter(
            by_U_ID=request.user.U_ID, isActive=True
        )
        if results.count() == 0:
            contexts["message"] = {
                    "type": "warning",
                    "message": "条件に一致するデータが1つもありませんでした。",
                }
        contexts["results"] = results
        contexts["th_all"] = current_menu["th_all"]

    elif control == "interview":
        options = [
            {
                "color": "outline-primary",
                "n_option": "date",
                "desc": "面談日時",
                "reverse": "",
            },
            {
                "color": "outline-primary",
                "n_option": "aspire",
                "desc": "志望度",
                "reverse": "",
            },
        ]
        contexts["options"] = options
        results = Interview.objects.filter(
            RegistID__by_U_ID=request.user.U_ID, RegistID__isActive=True
        )
        if results.count() == 0:
            contexts["message"] = {
                    "type": "warning",
                    "message": "条件に一致するデータが1つもありませんでした。",
                }
        contexts["results"] = results
        for o in options:
            if o["n_option"] == option:
                o["reverse"] = "_r"
                o["active"] = "active"
                contexts["results"] = sorted(
                    contexts["results"], key=lambda x, o=o: getattr(x, o["n_option"])
                )
            elif o["n_option"] + "_r" == option:
                o["reverse"] = ""
                o["active"] = "active"
                contexts["results"] = sorted(
                    contexts["results"],
                    key=lambda x, o=o: getattr(x, o["n_option"]),
                    reverse=True,
                )
                o["color"] = "warning"
            else:
                o["active"] = ""
        contexts["th_all"] = current_menu["th_all"]

    elif control == "R_aspire":
        R_sets = RegistSets.objects.filter(by_U_ID=request.user.U_ID, isActive=True)
        if R_sets.count() == 0:
            contexts["message"] = {
                    "type": "warning",
                    "message": "条件に一致するデータが1つもありませんでした。",
                }
        contexts["results"] = []
        for R in R_sets:
            contexts["results"].append(
                {
                    "R_sets": R,
                    "c_interview": Interview.objects.filter(RegistID=R, by_U_ID=request.user.U_ID).count(),
                    "sum_aspire": (
                        Interview.objects.filter(RegistID=R, by_U_ID=request.user.U_ID).aggregate(Sum("aspire"))[
                            "aspire__sum"
                        ]
                        if Interview.objects.filter(RegistID=R, by_U_ID=request.user.U_ID).aggregate(
                            Sum("aspire")
                        )["aspire__sum"]
                        is not None
                        else 0
                    ),
                    "avg_aspire": (
                        Interview.objects.filter(RegistID=R, by_U_ID=request.user.U_ID).aggregate(Avg("aspire"))[
                            "aspire__avg"
                        ]
                        if Interview.objects.filter(RegistID=R, by_U_ID=request.user.U_ID).aggregate(
                            Avg("aspire")
                        )["aspire__avg"]
                        is not None
                        else 0
                    ),
                }
            )
        options = [
            {
                "color": "outline-primary",
                "n_option": "c_interview",
                "desc": "面談回数",
                "reverse": "",
            },
            {
                "color": "outline-primary",
                "n_option": "sum_aspire",
                "desc": "合計志望度順",
                "reverse": "",
            },
            {
                "color": "outline-primary",
                "n_option": "avg_aspire",
                "desc": "平均志望度順",
                "reverse": "",
            },
        ]
        for o in options:
            if o["n_option"] == option:
                o["reverse"] = "_r"
                o["active"] = "active"
                contexts["results"] = sorted(
                    contexts["results"], key=lambda x, o=o: x[o["n_option"]]
                )
            elif o["n_option"] + "_r" == option:
                o["reverse"] = ""
                o["active"] = "active"
                contexts["results"] = sorted(
                    contexts["results"],
                    key=lambda x, o=o: x[o["n_option"]],
                    reverse=True,
                )
                o["color"] = "warning"
            else:
                o["active"] = ""
        contexts["options"] = options
        contexts["th_all"] = current_menu["th_all"]

    elif control == "cat_interview":
        results = Interview.objects.filter(
            RegistID__by_U_ID=request.user.U_ID, RegistID__isActive=True, by_U_ID=request.user.U_ID
        )
        if results.count() == 0:
            contexts["message"] = {
                    "type": "warning",
                    "message": "条件に一致するデータが1つもありませんでした。",
                }
        if option != "default":
            if results.filter(tag=option).count() == 0:
                contexts["message"] = {
                    "type": "warning",
                    "message": "条件に一致する面談録がありませんでした。",
                }
            else:
                results = results.filter(tag=option)
        contexts["results"] = results
        choices = Interview.tags
        contexts["choices"] = choices
        contexts["th_all"] = current_menu["th_all"]

    elif control == "top":
        contexts["message"] = {
            "type": "success",
            "message": "左のメニューから選択してください。(カスタムシートで指定した場合を除き、活動中の企業のみ表示されます)",
        }
    else:
        try:
            if control in [
                cs.sheet_name
                for cs in CustomSheet.objects.filter(by_U_ID=request.user.U_ID)
            ]:
                contexts["customsheet"] = "true"
                cs = CustomSheet.objects.get(sheet_name=control, by_U_ID=request.user.U_ID)
                results = apps.get_model("main", cs.model).objects.filter(by_U_ID=request.user.U_ID).all()
                if cs.search_settings != {}:
                    if cs.search_settings["how"] == "1":
                        results = results.filter(
                            **{f"{cs.search_settings['where']}": cs.search_settings["what"]}
                        )
                    elif cs.search_settings["how"] == "2":
                        results = results.filter(
                            **{
                                f"{cs.search_settings['where']}__contains": cs.search_settings[
                                    "what"
                                ]
                            }
                        )
                    elif cs.search_settings["how"] == "3":
                        results = results.filter(
                            **{
                                f"{cs.search_settings['where']}__gte": cs.search_settings[
                                    "what"
                                ]
                            }
                        )
                    elif cs.search_settings["how"] == "4":
                        results = results.filter(
                            **{
                                f"{cs.search_settings['where']}__lte": cs.search_settings[
                                    "what"
                                ]
                            }
                        )
                    elif cs.search_settings["how"] == "5":
                        results = results.exclude(
                            **{
                                f"{cs.search_settings['where']}": cs.search_settings[
                                    "what"
                                ]
                            }
                        )
                if cs.view_settings != {}:
                    if cs.view_settings[list(cs.view_settings.keys())[0]] == "1":
                        results = results.order_by(list(cs.view_settings.keys())[0])
                    elif cs.view_settings[list(cs.view_settings.keys())[0]] == "2":
                        results = results.order_by(
                            list(cs.view_settings.keys())[0]
                        ).reverse()
                if results.count() == 0:
                    if (cs.search_settings['where'] in ForeignKeySets):
                        raise Django_FieldError
                    contexts["message"] = {
                        "type": "warning",
                        "message": "条件に一致するデータが1つもありませんでした。",
                    }
                contexts["sheet_config"] = {
                    "model": cs.model,
                    "selected": cs.selected_field,
                    "view_settings": cs.view_settings,
                    "search_settings": cs.search_settings,
                    "sheet_id": cs.sheet_id,
                }
                contexts["results"] = results
                contexts["th_all"] = cs.selected_field
            else:
                contexts["message"] = {
                    "type": "danger",
                    "message": "不正なリクエストです。",
                }
        except Django_FieldError:
            if cs.search_settings['where'] in ForeignKeySets:
                cs.search_settings['where'] = ForeignKeySets[cs.search_settings['where']]
                cs.save()
            contexts["message"] = {
                "type": "info",
                "message": f"検索条件の自動修正を行いました。再度 '{control} ' を選択し直してください。\n\
                この画面が繰り返し表示される際は、問い合わせ機能から管理者へお問い合わせください",
            }

    contexts["menu"] = menu
    return render(request, "view/main.html", contexts)


@login_required
def create_custom_sheet(request):
    contexts = collect_regnum(request)
    contexts["model_names"] = {
        model.__name__: model._meta.verbose_name
        for model in apps.get_models()
        if model.__name__
        not in [
            "LogEntry",
            "Permission",
            "Group",
            "User",
            "CustomUser",
            "Session",
            "Site",
            "ContentType",
            "AdminLog",
            "CustomSheet",
            "InfomationModel",
            "SupportTicketModel",
            "RegistSets",
            "ESModel",
        ]
    }
    if "model" in request.GET:
        if request.GET["model"] == "default":
            return redirect("create_custom_sheet")
        if request.GET["create_sheet_name"] == "":
            contexts["message"] = {
                "type": "danger",
                "message": "シート名を入力してください",
            }
            return render(request, "view/customsheet/create.html", contexts)
        else:
            if (
                CustomSheet.objects.filter(
                    sheet_name=request.GET["create_sheet_name"]
                ).count()
                > 0
            ):
                contexts["message"] = {
                    "type": "danger",
                    "message": "そのシート名は既に使用されています。",
                }
                return render(request, "view/customsheet/create.html", contexts)
            contexts["model_selected"] = request.GET["model"]
            if request.GET["model"] not in contexts["model_names"]:
                contexts["message"] = {
                    "type": "danger",
                    "message": "不正なリクエストです。",
                }
                return render(request, "view/customsheet/create.html", contexts)
            model = apps.get_model("main", request.GET["model"])
            contexts["model_fields"] = {
                field.name: field.verbose_name if hasattr(field, 'verbose_name') else field.name
                for field in model._meta.get_fields()
                if field.name
                not in [
                    "id",
                    "RegistID",
                    "InterviewID",
                    "regist_publish",
                    "AdoptionID",
                    "D_CompanyID",
                    "MotivationID",
                    "IdeaID",
                    "AboutID",
                    "CompanyID",
                    "by_U_ID",
                    "registsets",
                    "ESlist",
                    "interviewer_id"
                ]
            }
            contexts["sheet_name_form"] = request.GET["create_sheet_name"]
            contexts["message"] = {
                "type": "success",
                "message": "選択したモデルを確認し、抽出対象のフィールドと、必要であれば表示名を指定してください",
            }

    if request.method == "POST":
        if request.POST["request_type"] == "select_model_and_field":
            res = {}
            for x, y in zip(request.POST.getlist("selected_field"), request.POST.getlist("selected_field_name")):
                res[x] = y
            contexts["selected_field"] = res
            contexts["model_fields"] = ""
            contexts["message"] = {
                "type": "success",
                "message": "指定したフィールドと表示名を確認し、表示順の指定、検索対象と検索条件を指定してください",
            }
        if request.POST["request_type"] == "view_setting":
            contexts["model_fields"] = ""
            data = {
                "create_sheet_name": request.POST.get("create_sheet_name"),
                "select_model": request.POST.get("model"),
                "selected_field": {
                    x: y
                    for x, y in zip(
                        request.POST.getlist("selected_field"),
                        request.POST.getlist("selected_field_name"),
                    )
                },
                "view_setting": request.POST.get("view_setting"),
                "view_setting_order": request.POST.get("view_setting_order"),
                "view_setting_search_how": request.POST.get("view_setting_search_how"),
                "view_setting_search": request.POST.get("view_setting_search"),
                "view_setting_search_string": request.POST.get(
                    "view_setting_search_string"
                ),
            }
            request.session["result_data"] = data
            contexts["result_data"] = data
            contexts["message"] = {
                "type": "success",
                "message": "以下の内容で登録されます。内容を確認してください",
            }
        if request.POST["request_type"] == "create_sheet":
            data = request.session["result_data"]
            CustomSheet.objects.create(
                sheet_id=secrets.token_hex(32),
                sheet_name=data["create_sheet_name"],
                model=data["select_model"],
                selected_field=data["selected_field"],
                view_settings=(
                    {data["view_setting"]: data["view_setting_order"]}
                    if data["view_setting"] != ""
                    else {}
                ),
                by_U_ID=request.user.U_ID,
                search_settings=(
                    {
                        "how": data["view_setting_search_how"],
                        "where": data["view_setting_search"],
                        "what": data["view_setting_search_string"],
                    }
                    if data["view_setting_search_how"] != ""
                    else {}
                ),
            )
            del request.session["result_data"]
            return HttpResponse(
                f"登録が完了しました。<a href ='{reverse('view_main', kwargs=dict(control='top',option='default' ))}'>戻る</a>"
            )
    return render(request, "view/customsheet/create.html", contexts)


@login_required
def delete_custom_sheet(request, id):
    contexts = collect_regnum(request)
    cs = CustomSheet.objects.get(sheet_id=id, by_U_ID=request.user.U_ID)
    contexts["sheet_config"] = {
        "model": cs.model,
        "selected": cs.selected_field,
        "view_settings": cs.view_settings,
        "search_settings": cs.search_settings,
        "sheet_id": cs.sheet_id,
    }
    if request.method == "POST":
        CustomSheet.objects.filter(sheet_id=id, by_U_ID=request.user.U_ID).delete()
        return HttpResponse(
            f"削除しています...<script>window.opener.location.href='{reverse('view_main', kwargs=dict(control='top',option='default' ))}'</script>"
        )
    return render(request, "view/customsheet/delete.html", contexts)


@login_required
def export_customsheet(request):
    contexts = collect_regnum(request)
    if request.method == "POST":
        c_all = CustomSheet.objects.filter(by_U_ID=request.user.U_ID)
        response = HttpResponse(content_type="application/json")
        sets = {"sheets": [model_to_dict(i) for i in c_all]}
        for s in sets["sheets"]:
            del s["by_U_ID"]
        response["Content-Disposition"] = (
                    "attachment; filename*=UTF-8''{}".format(
                        urllib.parse.quote(("export_custom_sheet.json").encode("utf8"))
                    )
                )
        response.write(json.dumps(sets, cls=DateTimeEncoder, ensure_ascii=False))
        return response
    return render(request, "view/export_customsheet.html", contexts)


@login_required
def import_customsheet(request):
    contexts = collect_regnum(request)
    if request.method == "POST":
        num_data = 0
        ok_data = 0
        name_ok_data = []
        name_ng_data = []
        try:
            data = json.loads(request.FILES["file"].read())
            for s in data["sheets"]:
                num_data += 1
                if CustomSheet.objects.filter(sheet_name=s["sheet_name"], by_U_ID=request.user.U_ID).count() > 0:
                    name_ng_data.append(s["sheet_name"])
                    continue
                CustomSheet.objects.create(
                    sheet_id=secrets.token_hex(32),
                    sheet_name=s["sheet_name"],
                    model=s["model"],
                    selected_field=s["selected_field"],
                    view_settings=s["view_settings"],
                    by_U_ID=request.user.U_ID,
                    search_settings=s["search_settings"],
                )
                name_ok_data.append(s["sheet_name"])
                ok_data += 1
        except UnicodeDecodeError:
            return HttpResponse("<p> ファイルの構成が不正です。</p>")
        contexts["num_data"] = num_data
        contexts["ok_data"] = ok_data
        contexts["name_ok_data"] = name_ok_data
        contexts["name_ng_data"] = name_ng_data
        return render(request, "view/import_result.html", contexts)
    return render(request, "view/import_customsheet.html", contexts)
