from django.test import Client
from django.urls import reverse
from authUser.models import CustomUser as User
import main.models as main_models
import django.urls.exceptions as url_exceptions
from datetime import datetime
import pytz

def test_user_init(user):
    client = Client()
    client.force_login(user)
    return client


def test_anonymous_init():
    client = Client()
    return client


def cannot_access(url, client, **uargs):
    """
    アクセスを拒否された際にTrueを返す
    """
    if uargs:
        response = client.get(reverse(url, args=uargs["uargs"]))
    else:
        response = client.get(reverse(url))
    if response.status_code == 403 or response.status_code == 302:
        return True
    return False


def can_access(url, client, **uargs):
    """
    アクセスできる場合にTrueを返す
    """
    if uargs:
        response = client.get(reverse(url, args=uargs["uargs"]))
    else:
        response = client.get(reverse(url))
    if response.status_code == 200:
        return True
    return False


def is_error(url, client, **uargs):
    """
    存在しない場合にTrueを返す
    """
    try:
        if uargs:
            response = client.get(reverse(url, args=uargs["uargs"]))
        else:
            response = client.get(reverse(url))
    except url_exceptions.NoReverseMatch:
        return True
    return False


def create_admin(**another):
    if another:
        user = User.objects.create_superuser(username='admin_test_user+1', password='admin123', email='admin@example.com', y_graduation=2026, U_ID="default_U_ID+1")
    else:
        user = User.objects.create_superuser(username='admin_test_user', password='admin123', email='admin@example.com', y_graduation=2026, U_ID="default_U_ID")
    return user


def create_user(**another):
    if another:
        user = User.objects.create_user(username='test_user+1', password='admin123', email='admin@example.com', y_graduation=2026, U_ID="default_U_ID+1")
    else:
        user = User.objects.create_user(username='test_user', password='admin123', email='admin@example.com', y_graduation=2026, U_ID="default_U_ID")
    return user


def create_post(**client):
    if not client:
        client = create_user()
    else:
        client = client["client"]
    t_company = main_models.Companies.objects.create(
        by_U_ID=client.U_ID,
        name="test_com",
        industry="test",
        president="name",
        contact="name",
        Ca_year=2026,
        CompanyID="test_com_ID"
        )
    post = main_models.RegistSets.objects.create(
                                                RegistID="test",
                                                by_U_ID=client.U_ID,
                                                company=t_company,
                                                about=main_models.About.objects.create(
                                                                                            by_U_ID=client.U_ID,
                                                                                            AboutID="test_about",
                                                                                            company_name=t_company
                                                                                            ),
                                                idea=main_models.Idea.objects.create(
                                                                                            by_U_ID=client.U_ID,
                                                                                            IdeaID="test_idea",
                                                                                            company_name=t_company
                                                                                            ),
                                                motivation=main_models.Motivation.objects.create(
                                                                                            by_U_ID=client.U_ID,
                                                                                            MotivationID="test_motivation",
                                                                                            company_name=t_company
                                                ),
                                                d_company=main_models.D_Company.objects.create(
                                                                                            by_U_ID=client.U_ID,
                                                                                            D_CompanyID="test_d_company",
                                                                                            company_name=t_company
                                                ),
                                                adoption=main_models.Adoption.objects.create(
                                                                                            by_U_ID=client.U_ID,
                                                                                            AdoptionID="test_adoption",
                                                                                            company_name=t_company
                                                ),
                                                )
    return post


def create_interview(post, **client):
    if not client:
        client = create_user()
    else:
        client = client["client"]

    interview = main_models.Interview.objects.create(
                                                    by_U_ID=client.U_ID,
                                                    InterviewID="test_interview",
                                                    company_name=post.company,
                                                    RegistID=post,
                                                    title="test_title",
                                                    date=datetime.now(pytz.timezone('Asia/Tokyo')),
                                                    )
    return interview
