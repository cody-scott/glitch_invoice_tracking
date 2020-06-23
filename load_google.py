import os
from dotenv import load_dotenv
load_dotenv()

g_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
g_data = os.getenv('GOOGLE_CREDENTIALS')

with open(g_path, 'w') as fl:
    fl.write(g_data)
