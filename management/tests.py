from django.test import TestCase
import testasset as ta
# Create your tests here.


class ManagementTestCase(TestCase):

    def test_index(self):
        print(f"\n{self.__str__()}")
        ta.only_admin_user(self, "management")
    
    def test_all_sheets(self):
        print(f"\n{self.__str__()}")
        ta.only_admin_user(self, "all_sheets")
    
    def test_management_sheets(self):
        print(f"\n{self.__str__()}")
        ta.only_admin_user(self, "management_sheets")
    
    def test_all_interviewer(self):
        print(f"\n{self.__str__()}")
        ta.only_admin_user(self, "all_interviewer")
    
    def test_admin_all_sheet(self):
        print(f"\n{self.__str__()}")
        url = "admin_all_sheet"
        u = ta.create_user()
        a = ta.create_admin()
        user = ta.test_user_init(u)
        admin = ta.test_user_init(a)
        anonymous = ta.test_anonymous_init()
        self.assertEqual(ta.is_error(url, user, uargs={"sheet_from": "企業名", "where": "a"}), False)
        self.assertEqual(ta.is_error(url, admin, uargs={"sheet_from": "企業名", "where": "a"}), False)
        self.assertEqual(ta.is_error(url, anonymous, uargs={"sheet_from": "企業名", "where": "a"}), False)
        self.assertEqual(ta.can_access(url, user, uargs={"sheet_from": "企業名", "where": "a"}), False)
        self.assertEqual(ta.can_access(url, admin, uargs={"sheet_from": "企業名", "where": "a"}), True)
        self.assertEqual(ta.can_access(url, anonymous, uargs={"sheet_from": "企業名", "where": "a"}), False)
        self.assertEqual(ta.cannot_access(url, user, uargs={"sheet_from": "企業名", "where": "a"}), True)
        self.assertEqual(ta.cannot_access(url, admin, uargs={"sheet_from": "企業名", "where": "a"}), False)
        self.assertEqual(ta.cannot_access(url, anonymous, uargs={"sheet_from": "企業名", "where": "a"}), True)
