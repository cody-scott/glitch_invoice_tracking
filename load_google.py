import os


def load_g_data():
    # cheat it since i have a local file of creds
    if os.getenv("LOCAL") is not None:
        return

    g_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    g_data = os.getenv('GOOGLE_CREDENTIALS')
    
    with open(g_path, 'w') as fl:
        fl.write(g_data)
