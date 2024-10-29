from django.test import TestCase
import testasset as ta
# Create your tests here.


class TaskCakenderTestCase(TestCase):
    def test_calender_main(self):
        print(f"\n{self.__str__()}")
        ta.only_login_user(self, "calendar_main")

    def test_new_task(self):
        print(f"\n{self.__str__()}")
        ta.only_login_user(self, "new_task")
