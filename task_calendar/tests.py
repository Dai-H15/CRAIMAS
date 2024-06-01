from django.test import TestCase
import testasset as ta
# Create your tests here.


class TaskCakenderTestCase(TestCase):
    def test_calender_main(self):
        ta.only_login_user(self, "calendar_main")
