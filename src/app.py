import os

from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

from libs.bsky import BskyClient


HANDLE = os.getenv("HANDLE")
PASSWORD = os.getenv("APPPASS")


def main():
    bc = BskyClient(HANDLE, PASSWORD)
    bc.run()


if __name__ == "__main__":
    main()
