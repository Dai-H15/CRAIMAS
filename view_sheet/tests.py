from django.test import TestCase
from .models import CustomSheet
import testasset
import secrets


# Create your tests here.
class CustomSheetTest(TestCase):
    def test_view_policy(self):
        print(f"\n{self.__str__()}")
        user1 = testasset.create_user(another=1)
        user2 = testasset.create_user(another=2)
        user1_custom = CustomSheet.objects.create(
            sheet_id=secrets.token_hex(32),
            by_U_ID=user1.U_ID,
            sheet_name="test",
            model="Adoption",
            selected_field={"company_name": "企業名", "occupation": "採用職種", "from_url": "採用情報URL", "salary": "新卒初任給"},
            view_settings={"salary": "2"},
            search_settings={}
        )
        user2_custom = CustomSheet.objects.create(
            sheet_id=secrets.token_hex(32),
            by_U_ID=user2.U_ID,
            sheet_name="test",
            model="Adoption",
            selected_field={"company_name": "企業名", "occupation": "採用職種", "from_url": "採用情報URL", "salary": "新卒初任給"},
            view_settings={"salary": "2"},
            search_settings={}
        )
        client1 = testasset.test_user_init(user1)
        client2 = testasset.test_user_init(user2)
        self.assertEqual(testasset.can_access(
            url="view_main",
            client=client1,
            uargs=[f"{user1_custom.sheet_id}", "default"]),
            True)
        self.assertEqual(testasset.cannot_access(
            url="view_main",
            client=client2,
            uargs=[f"{user1_custom.sheet_id}", "default"]),
            True)
        self.assertEqual(testasset.can_access(
            url="view_main",
            client=client2,
            uargs=[f"{user2_custom.sheet_id}", "default"]),
            True)
        self.assertEqual(testasset.cannot_access(
            url="view_main",
            client=client1,
            uargs=[f"{user2_custom.sheet_id}", "default"]),
            True)
