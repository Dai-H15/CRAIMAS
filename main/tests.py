from django.test import TestCase
import testasset


def all_user(self, url):
    u = testasset.create_user()
    a = testasset.create_admin()
    user = testasset.test_user_init(u)
    admin = testasset.test_user_init(a)
    anonymous = testasset.test_anonymous_init()
    self.assertEqual(testasset.is_error(url, user), False)
    self.assertEqual(testasset.is_error(url, admin), False)
    self.assertEqual(testasset.is_error(url, anonymous), False)
    self.assertEqual(testasset.can_access(url, user), True)
    self.assertEqual(testasset.can_access(url, admin), True)
    self.assertEqual(testasset.can_access(url, anonymous), True)
    self.assertEqual(testasset.cannot_access(url, user), False)
    self.assertEqual(testasset.cannot_access(url, admin), False)
    self.assertEqual(testasset.cannot_access(url, anonymous), False)


def only_login_user(self, url, **uargs):
    if uargs:
        u = testasset.create_user(another=1)
    else:
        u = testasset.create_user()
    if uargs:
        a = testasset.create_admin(another=1)
    else:
        a = testasset.create_admin()
    user = testasset.test_user_init(u)
    admin = testasset.test_user_init(a)
    anonymous = testasset.test_anonymous_init()
    self.assertEqual(testasset.is_error(url, user), False)
    self.assertEqual(testasset.is_error(url, admin), False)
    self.assertEqual(testasset.is_error(url, anonymous), False)
    self.assertEqual(testasset.can_access(url, user), True)
    self.assertEqual(testasset.can_access(url, admin), True)
    self.assertEqual(testasset.can_access(url, anonymous), False)
    self.assertEqual(testasset.cannot_access(url, user), False)
    self.assertEqual(testasset.cannot_access(url, admin), False)
    self.assertEqual(testasset.cannot_access(url, anonymous), True)


def only_login_user_no_data(self, url, **uargs):
    """
    データがない場合のテスト。リダイレクト、若しくは何かしらのHTTPレスポンスがある場合
    """
    if uargs:
        u = testasset.create_user(another=1)
    else:
        u = testasset.create_user()
    if uargs:
        a = testasset.create_admin(another=1)
    else:
        a = testasset.create_admin()
    user = testasset.test_user_init(u)
    admin = testasset.test_user_init(a)
    anonymous = testasset.test_anonymous_init()
    self.assertEqual(testasset.is_error(url, user), True)
    self.assertEqual(testasset.is_error(url, admin), True)
    self.assertEqual(testasset.is_error(url, anonymous), True)
    self.assertEqual(testasset.can_access(url, user), True)
    self.assertEqual(testasset.can_access(url, admin), True)
    self.assertEqual(testasset.can_access(url, anonymous), False)
    self.assertEqual(testasset.cannot_access(url, user), False)
    self.assertEqual(testasset.cannot_access(url, admin), False)
    self.assertEqual(testasset.cannot_access(url, anonymous), True)


def only_admin_user(self, url):
    u = testasset.create_user()
    a = testasset.create_admin()
    user = testasset.test_user_init(u)
    admin = testasset.test_user_init(a)
    anonymous = testasset.test_anonymous_init()
    self.assertEqual(testasset.is_error(url, user), False)
    self.assertEqual(testasset.is_error(url, admin), False)
    self.assertEqual(testasset.is_error(url, anonymous), False)
    self.assertEqual(testasset.can_access(url, user), False)
    self.assertEqual(testasset.can_access(url, admin), True)
    self.assertEqual(testasset.can_access(url, anonymous), False)
    self.assertEqual(testasset.cannot_access(url, user), True)
    self.assertEqual(testasset.cannot_access(url, admin), False)
    self.assertEqual(testasset.cannot_access(url, anonymous), True)


def only_login_user_with_post(self, url):
    u = testasset.create_user()
    a = testasset.create_admin()
    user = testasset.test_user_init(u)
    admin = testasset.test_user_init(a)
    anonymous = testasset.test_anonymous_init()
    post = testasset.create_post(client=u)
    self.assertEqual(testasset.is_error(url, user, uargs=[post.RegistID]), False)
    self.assertEqual(testasset.is_error(url, admin, uargs=[post.RegistID]), False)
    self.assertEqual(testasset.is_error(url, anonymous, uargs=[post.RegistID]), False)
    self.assertEqual(testasset.can_access(url, user, uargs=[post.RegistID]), True)
    self.assertEqual(testasset.can_access(url, admin, uargs=[post.RegistID]), True)
    self.assertEqual(testasset.can_access(url, anonymous, uargs=[post.RegistID]), False)
    self.assertEqual(testasset.cannot_access(url, user, uargs=[post.RegistID]), False)
    self.assertEqual(testasset.cannot_access(url, admin, uargs=[post.RegistID]), False)
    self.assertEqual(testasset.cannot_access(url, anonymous, uargs=[post.RegistID]), True)


def only_login_user_with_interview(self, url):
    u = testasset.create_user()
    a = testasset.create_admin()
    user = testasset.test_user_init(u)
    admin = testasset.test_user_init(a)
    anonymous = testasset.test_anonymous_init()
    post = testasset.create_post(client=u)
    interview = testasset.create_interview(post, client=u)
    self.assertEqual(testasset.is_error(url, user, uargs=[interview.InterviewID]), False)
    self.assertEqual(testasset.is_error(url, admin, uargs=[interview.InterviewID]), False)
    self.assertEqual(testasset.is_error(url, anonymous, uargs=[interview.InterviewID]), False)
    self.assertEqual(testasset.can_access(url, user, uargs=[interview.InterviewID]), True)
    self.assertEqual(testasset.can_access(url, admin, uargs=[interview.InterviewID]), True)
    self.assertEqual(testasset.can_access(url, anonymous, uargs=[interview.InterviewID]), False)
    self.assertEqual(testasset.cannot_access(url, user, uargs=[interview.InterviewID]), False)
    self.assertEqual(testasset.cannot_access(url, admin, uargs=[interview.InterviewID]), False)
    self.assertEqual(testasset.cannot_access(url, anonymous, uargs=[interview.InterviewID]), True)


def only_login_user_with_args(self, url, args):
    """
    URLにて渡す必要がある値が存在する際に使用するテストセット。
    エラーが発生することなく、ログインが必要（リダイレクトが行われるなどで回避される）なページのテスト
    """
    u = testasset.create_user()
    a = testasset.create_admin()
    user = testasset.test_user_init(u)
    admin = testasset.test_user_init(a)
    anonymous = testasset.test_anonymous_init()
    self.assertEqual(testasset.is_error(url, user, uargs=args), False)
    self.assertEqual(testasset.is_error(url, admin, uargs=args), False)
    self.assertEqual(testasset.is_error(url, anonymous, uargs=args), False)
    self.assertEqual(testasset.can_access(url, user, uargs=args), True)
    self.assertEqual(testasset.can_access(url, admin, uargs=args), True)
    self.assertEqual(testasset.can_access(url, anonymous, uargs=args), False)
    self.assertEqual(testasset.cannot_access(url, user, uargs=args), False)
    self.assertEqual(testasset.cannot_access(url, admin, uargs=args), False)
    self.assertEqual(testasset.cannot_access(url, anonymous, uargs=args), True)


class MainViewTests(TestCase):
    def test_index(self):
        all_user(self, "index")

    def test_regist_base(self):
        only_login_user(self, "regist_base")

    def test_mypage(self):
        only_login_user(self, "mypage")

    def test_regist_all(self):
        only_login_user(self, "regist_all")

    def test_view_my_post(self):
        only_login_user_with_post(self, "view_my_post")

    def test_view_my_post_no_args(self):
        testasset.is_error("view_my_post", testasset.test_user_init(testasset.create_user()))
        only_login_user(self, "create_company", uargs=1)

    def test_delete_posts(self):
        only_login_user_with_post(self, "delete_posts")

    def test_delete_posts_no_args(self):
        testasset.is_error("delete_posts", testasset.test_user_init(testasset.create_user()))
        only_login_user(self, "create_company", uargs=1)

    def test_edit_posts(self):
        only_login_user_with_post(self, "edit_posts")

    def test_edit_posts_no_args(self):
        testasset.is_error("edit_posts", testasset.test_user_init(testasset.create_user()))
        only_login_user(self, "create_company", uargs=1)

    def test_regist_sets(self):
        only_login_user(self, "regist_sets")

    def test_create_company(self):
        only_login_user(self, "create_company")

    def test_import_company(self):
        only_login_user(self, "import_company")

    def test_search_company_no_args(self):
        testasset.is_error("search_company", testasset.test_user_init(testasset.create_user()))
        testasset.is_error("search_company", testasset.test_anonymous_init())

    def test_set_sarched_data(self):
        only_login_user(self, "import_company")

    def test_get_address(self):
        only_login_user_with_args(self, "get_address", args={"zipcode": "1100000"})

    def test_interview_main(self):
        only_login_user_with_post(self, "interview_main")

    def test_interview_create(self):
        only_login_user_with_post(self, "interview_create")

    def test_view_interview(self):
        only_login_user_with_interview(self, "view_interview")

    def test_delete_interview(self):
        only_login_user_with_interview(self, "delete_interview")

    def test_calc(self):
        only_login_user(self, "calc")

    def test_export_sheet(self):
        only_login_user_with_post(self, "export_sheet")

    def test_json_import(self):
        only_login_user(self, "json_import")

    def test_change_active(self):
        only_login_user(self, "change_active")

    def test_get_interviewer(self):
        only_login_user_with_post(self, "get_interviewer")

    def test_prof_interviewer(self):
        url = "prof_interviewer"
        u = testasset.create_user()
        a = testasset.create_admin()
        user = testasset.test_user_init(u)
        admin = testasset.test_user_init(a)
        anonymous = testasset.test_anonymous_init()
        post = testasset.create_post(client=u)
        self.assertEqual(testasset.is_error(url, user, uargs={"company_id": post.company, "i_name": "hoge"}), False)
        self.assertEqual(testasset.is_error(url, admin, uargs={"company_id": post.company, "i_name": "hoge"}), False)
        self.assertEqual(testasset.is_error(url, anonymous, uargs={"company_id": post.company, "i_name": "hoge"}), False)
        self.assertEqual(testasset.can_access(url, user, uargs={"company_id": post.company, "i_name": "hoge"}), True)
        self.assertEqual(testasset.can_access(url, admin, uargs={"company_id": post.company, "i_name": "hoge"}), True)
        self.assertEqual(testasset.can_access(url, anonymous, uargs={"company_id": post.company, "i_name": "hoge"}), False)
        self.assertEqual(testasset.cannot_access(url, user, uargs={"company_id": post.company, "i_name": "hoge"}), False)
        self.assertEqual(testasset.cannot_access(url, admin, uargs={"company_id": post.company, "i_name": "hoge"}), False)
        self.assertEqual(testasset.cannot_access(url, anonymous, uargs={"company_id": post.company, "i_name": "hoge"}), True)

    def test_search_post(self):
        url = "search_post"
        u = testasset.create_user()
        a = testasset.create_admin()
        user = testasset.test_user_init(u)
        admin = testasset.test_user_init(a)
        anonymous = testasset.test_anonymous_init()
        self.assertEqual(testasset.is_error(url, user, uargs={"sheet_from": "企業名", "where": "a"}), False)
        self.assertEqual(testasset.is_error(url, admin, uargs={"sheet_from": "企業名", "where": "a"}), False)
        self.assertEqual(testasset.is_error(url, anonymous, uargs={"sheet_from": "企業名", "where": "a"}), False)
        self.assertEqual(testasset.can_access(url, user, uargs={"sheet_from": "企業名", "where": "a"}), True)
        self.assertEqual(testasset.can_access(url, admin, uargs={"sheet_from": "企業名", "where": "a"}), True)
        self.assertEqual(testasset.can_access(url, anonymous, uargs={"sheet_from": "企業名", "where": "a"}), False)
        self.assertEqual(testasset.cannot_access(url, user, uargs={"sheet_from": "企業名", "where": "a"}), False)
        self.assertEqual(testasset.cannot_access(url, admin, uargs={"sheet_from": "企業名", "where": "a"}), False)
        self.assertEqual(testasset.cannot_access(url, anonymous, uargs={"sheet_from": "企業名", "where": "a"}), True)