import os

from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# from .keep_alive import keep_alive
from libs.bsky import BskyClient


HANDLE = os.getenv("HANDLE")
PASSWORD = os.getenv("APPPASS")


def main():
    # keep_alive()
    bc = BskyClient(HANDLE, PASSWORD)
    bc.run()


if __name__ == "__main__":
    main()
