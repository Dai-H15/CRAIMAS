from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

CustomUser = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [CustomUser.USERNAME_FIELD] + CustomUser.REQUIRED_FIELDS + ['password1', 'password2']
        labels = {"y_graduation": "卒業(見込)年度",
                  "gBIZINFO_key": "gBizINFO Web APIキー ",
                  "email": "メールアドレス (大学メールアドレスをお持ちの方はそちらを使用してください。)"}


class LoginForm(AuthenticationForm):
    pass
