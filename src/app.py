import os

from dotenv import load_dotenv

from libs.bsky import BskyClient
from libs.keep_alive import keep_alive

load_dotenv(verbose=True)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

HANDLE = os.getenv("HANDLE")
PASSWORD = os.getenv("APPPASS")


def main():
    keep_alive()
    bc = BskyClient(HANDLE, PASSWORD)
    print("Run bot")
    bc.run()


if __name__ == "__main__":
    main()
