import time

from atproto_client import Client
from atproto_client.models.app.bsky.feed.post import ReplyRef
from atproto_client.models import ComAtprotoRepoStrongRef

from .writing_prompts import WritingPromptProvider
from .prompt_image_generator import PromptImageGenerator


class BskyClient:
    def __init__(self, handle: str, password: str):
        self.handle = handle
        self.password = password
        self.client: Client = self._login()
        self.wp = WritingPromptProvider()
        print(f"Login: @{handle}")

    def _login(self) -> Client:
        c = Client()
        c.login(self.handle, self.password)
        return c

    def _get_notifications(self) -> list:
        res = self.client.app.bsky.notification.list_notifications()
        return res.notifications

    def _get_mention_and_replies(self) -> list:
        n = self._get_notifications()
        return [p for p in n if p.reason in ("mention", "reply") and not p.is_read]

    def _get_posts(self, ns):
        uris = [n.uri for n in ns]
        if not uris:
            return
        posts = self.client.app.bsky.feed.get_posts({"uris": uris})
        for post in posts.posts:
            yield post

    @staticmethod
    def approve_reply(post_view):
        v = post_view.author.viewer
        if v.blocked_by or v.blocking or v.blocking_by_list or not v.followed_by:
            return False
        return True

    def reply_to_as_dict(self, post):
        parent = {"cid": post.cid, "uri": post.uri}
        return {"root": parent, "parent": parent}

    def reply_to(self, post) -> ReplyRef:
        parent = ComAtprotoRepoStrongRef.Main(cid=post.cid, uri=post.uri)
        return ReplyRef(parent=parent, root=parent)

    @staticmethod
    def find_byte_position(text, substring):
        # 文字列をUTF-8でバイト列に変換
        byte_text = text.encode("utf-8")
        byte_substring = substring.encode("utf-8")
        # バイト列内での位置を検索
        start_position = byte_text.find(byte_substring)
        if start_position != -1:
            end_position = start_position + len(byte_substring)
            return {"byteStart": start_position, "byteEnd": end_position}
        return {"byteStart": -1, "byteEnd": -1}

    def _create_post_with_img(self, contents, img, ref_post, facets):
        self.client.send_image(
            text=contents, image=img, image_alt="", reply_to=ref_post, facets=facets
        )

    def _monitor_notifications(self):
        notifications = self._get_mention_and_replies()
        tag = "#ランダム書写お題"
        cnt = len(notifications) // 25 + 1
        for i in range(cnt):
            for post in self._get_posts(notifications[25 * i : 25 * (i + 1)]):
                if post.reply_count > 0:
                    continue
                contents = self.wp.choice()
                url = contents["url"]
                pig = PromptImageGenerator(contents)
                img = pig.gen_image()
                post_lines = [f"『{contents['title']}』{contents['author']}", tag]
                text = "\n".join(post_lines)
                ref = self.reply_to(post)
                facets = [
                    {
                        "index": self.find_byte_position(text, contents["title"]),
                        "features": [
                            {"$type": "app.bsky.richtext.facet#link", "uri": url}
                        ],
                    },
                    {
                        "index": self.find_byte_position(text, tag),
                        "features": [
                            {
                                "$type": "app.bsky.richtext.facet#tag",
                                "tag": tag.strip("#"),
                            }
                        ],
                    },
                ]
                self._create_post_with_img(
                    contents=text, img=img, ref_post=ref, facets=facets
                )
                print("Done")

    def run(self):
        while True:
            try:
                self._monitor_notifications()
            except Exception as e:
                print(f"An error occurred: {e}")
                self.client = self._login()
            finally:
                time.sleep(10)
