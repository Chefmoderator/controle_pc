import os
try:
    from dotenv import load_dotenv
except:
    os.system("python -m pip install python-dotenv")
    from dotenv import load_dotenv
load_dotenv()
class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")

def load_config():
    return Config()