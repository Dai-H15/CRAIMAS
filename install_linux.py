import os
import secrets, string
if not os.path.exists("settings/local_settings.py"):
    print("local_settings.py is creating...")
    with open("settings/local_settings.py", "w") as f:
        chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + "_@#&!?-#$"
        passw = "".join([secrets.choice(chars) for _ in range(50)])
        f.write(f"SECRET_KEY = '{passw}'\n")
        from cryptography.fernet import Fernet
        sec = Fernet.generate_key()
        f.write(f"ENCRYPT_KEY = {sec}\n")
        if input("is this DEV server ? y/n >>>") == "n":
            f.write(f"PG_PSWD = {'pls insert here'}\n")
        f.close()
