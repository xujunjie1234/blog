<<<<<<< HEAD
from myblog import create_app
=======
# from myblog import create_app
>>>>>>> 81a697f5407e67c391ca57ac677892e6f11f1b53

from dotenv import load_dotenv
import os

dotenv_path = os.path.join(os.path.dirname(__file__),".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

app = create_app('production')
