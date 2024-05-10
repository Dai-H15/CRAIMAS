import os
import secrets, string

user_os = input("Linux (0)? Windows (1)?\n>>>")

input("必要なライブラリをインストールします。Enterを押してください。")

if user_os == "0":
    os.system("pip install -r requirements.txt")
elif user_os == "1":
    os.system("python -m pip install -r requirements.txt")

print("インストールが完了しました。")

input("local_settings.pyを作成します。Enterを押してください。")

with open("settings/local_settings.py", "w") as f:
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + "_@#&!?-#$"
    passw = "".join([secrets.choice(chars) for _ in range(50)])
    f.write(f"SECRET_KEY = '{passw}'\n")
    f.close()


input("SQLite3にてデータベースを作成します。Enterを押してください。")
if user_os == "0":
    os.system("python3 manage.py makemigrations main view_sheet task_calendar authUser")
    os.system("python3 manage.py migrate")
if user_os == "1":
    os.system("python manage.py makemigrations main view_sheet task_calendar authUser")
    os.system("python manage.py migrate")

print("データベースの作成が完了しました。")

input("スーパーユーザーを作成します。Enterを押してください。")
if user_os == "0":
    os.system("python3 manage.py createsuperuser")
if user_os == "1":
    os.system("python manage.py createsuperuser")

print("スーパーユーザーの作成が完了しました。")