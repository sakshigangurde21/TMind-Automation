# test_env.py
from dotenv import load_dotenv
import os

load_dotenv()

print("BASE_URL:", os.environ.get('BASE_URL'))
print("USER_EMAIL:", os.environ.get('USER_EMAIL'))
print("PASSWORD:", os.environ.get('PASSWORD'))