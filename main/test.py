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
        print(f"\n{self.__str__()}")
        all_user(self, "index")
    def test_regist_base(self):
        print(f"\n{self.__str__()}")
        only_login_user(self, "regist_base")

    def test_mypage(self):
        print(f"\n{self.__str__()}")
        only_login_user(self, "mypage")

    def test_regist_all(self):
        print(f"\n{self.__str__()}")
        only_login_user(self, "regist_all")

    def test_view_my_post(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_post(self, "view_my_post")

    def test_view_my_post_no_args(self):
        print(f"\n{self.__str__()}")
        testasset.is_error("view_my_post", testasset.test_user_init(testasset.create_user()))

    def test_delete_posts(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_post(self, "delete_posts")

    def test_delete_posts_no_args(self):
        print(f"\n{self.__str__()}")
        testasset.is_error("delete_posts", testasset.test_user_init(testasset.create_user()))

    def test_edit_posts(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_post(self, "edit_posts")

    def test_edit_posts_no_args(self):
        print(f"\n{self.__str__()}")
        testasset.is_error("edit_posts", testasset.test_user_init(testasset.create_user()))

    def test_search_company_no_args(self):
        print(f"\n{self.__str__()}")
        testasset.is_error("search_company", testasset.test_user_init(testasset.create_user()))
        testasset.is_error("search_company", testasset.test_anonymous_init())

    def test_get_address(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_args(self, "get_address", args={"zipcode": "1100000"})

    def test_interview_main(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_post(self, "interview_main")

    def test_interview_create(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_post(self, "interview_create")

    def test_view_interview(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_interview(self, "view_interview")

    def test_delete_interview(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_interview(self, "delete_interview")

    def test_calc(self):
        print(f"\n{self.__str__()}")
        only_login_user(self, "calc")

    def test_export_sheet(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_post(self, "export_sheet")

    def test_json_import(self):
        print(f"\n{self.__str__()}")
        only_login_user(self, "json_import")

    def test_change_active(self):
        print(f"\n{self.__str__()}")
        only_login_user(self, "change_active")

    def test_get_interviewer(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_post(self, "get_interviewer")

    def test_prof_interviewer(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_args(self, "prof_interviewer", args={"company_id": "dummy", "i_id": "hoge"})

    def test_search_interviewer(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_args(self, "search_interviewer", args={"company_id": "dummy", "i_name": "dummy"})

    def test_search_post(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_args(self, "search_post", args={"sheet_from": "企業名", "where": "a"})

    def test_show_interview_num_zero(self):
        print(f"\n{self.__str__()}")
        url = "mypage"
        u = testasset.create_user()
        user = testasset.test_user_init(u)
        self.assertEqual(testasset.is_error(url, user), False)

    def test_show_interview_num_one(self):
        print(f"\n{self.__str__()}")
        url = "mypage"
        u = testasset.create_user()
        user = testasset.test_user_init(u)
        post = testasset.create_post(client=u)
        testasset.create_interview(post, client=u)
        self.assertEqual(testasset.is_error(url, user), False)

    def test_ES_index(self):
        print(f"\n{self.__str__()}")
        only_login_user(self, "ES_index")

    def test_ES_regist(self):
        print(f"\n{self.__str__()}")
        only_login_user(self, "ES_regist")

    def test_ES_show(self):
        print(f"\n{self.__str__()}")
        only_login_user(self, "ES_show")

    def test_ES_get_data(self):
        print(f"\n{self.__str__()}")
        only_login_user(self, "ES_get_data")

    def test_ES_show_detail(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_args(self, "ES_show_detail", args={"id": "dummy"})

    def test_ES_search(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_args(self, "ES_search", args={"to": "dummy", "what": "dummy"})

    def test_ES_delete(self):
        print(f"\n{self.__str__()}")
        only_login_user_with_args(self, "ES_delete", args={"id": "dummy"})

    def test_get_summary(self):
        print(f"\n{self.__str__()}")
        only_login_user(self, "get_summary")