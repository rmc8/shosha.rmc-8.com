import os
import traceback

import requests
from dotenv import load_dotenv

from libs.bsky import BskyClient
from libs.keep_alive import keep_alive

load_dotenv(verbose=True)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

HANDLE = os.getenv("HANDLE")
PASSWORD = os.getenv("APPPASS")
NOTIFICATION_URL = os.getenv("RND_SHOSHA_URL")


def main():
    keep_alive()
    bc = BskyClient(HANDLE, PASSWORD)
    try:
        print("Run bot")
        bc.run()
    except Exception as e:
        print(e)
        msg: str = traceback.format_exc()
        payload = {"error_msg": msg}
        headers = {"Content-Type": "application/json"}
        requests.post(NOTIFICATION_URL, json=payload, headers=headers)


if __name__ == "__main__":
    main()
