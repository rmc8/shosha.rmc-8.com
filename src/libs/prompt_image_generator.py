import io
from typing import List

from PIL import Image, ImageDraw, ImageFont

FONT_NORMAL_PATH = "assets/font/NotoSerifJP-Medium.otf"
FONT_BOLD_PATH = "assets/font/NotoSerifJP-Bold.otf"
NORMAL_FONT_SIZE = 32
BIG_FONT_SIZE = 48
LINE_HEIGHT = 32
PADDING = 64
AUTHOR_PADDING = 110
SCRIPT_PADDING = 110
SCRIPT_MARGIN_TOP = 32


class PromptImageGenerator:
    def __init__(self, contents):
        self.contents = contents
        self.font_normal = ImageFont.truetype(FONT_NORMAL_PATH, NORMAL_FONT_SIZE)
        self.font_bold = ImageFont.truetype(FONT_BOLD_PATH, BIG_FONT_SIZE)

    @staticmethod
    def _get_lines(text: str, length: int = 30) -> List[str]:
        lines: List[str] = []
        while text:
            if len(text) > length:
                # 最後のスペースの位置を見つけて行を分割する
                split_index = text.rfind(" ", 0, length)
                if split_index == -1:  # スペースが見つからない場合
                    split_index = length

                # 特定の記号を考慮して行を調整
                if text[split_index] in {"、", "。"}:
                    split_index += 1
                elif text[split_index : split_index + 2] == "。」":
                    split_index += 2

                line = text[:split_index].strip()
                text = text[split_index:].strip()
            else:
                line = text
                text = ""
            lines.append(line)
        return lines

    def gen_image(self):
        # Contents
        script = self.contents["script"]
        meta = self.contents
        del meta["script"]
        del meta["url"]
        lines = self._get_lines(script)

        # Create image
        meta_height = (len(meta.items())) * (BIG_FONT_SIZE + LINE_HEIGHT)
        padding_height = PADDING * 2
        script_height = (
            len(lines) * (NORMAL_FONT_SIZE + LINE_HEIGHT) + SCRIPT_MARGIN_TOP
        )
        height = meta_height + padding_height + script_height
        img = Image.new("RGB", size=(1200, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)

        # Meta
        for n, (key, val) in enumerate(meta.items()):
            text = f"『{val}』" if key == "title" else val
            x = PADDING if key == "title" else AUTHOR_PADDING
            draw.text(
                (x, PADDING + (n * (BIG_FONT_SIZE + LINE_HEIGHT))),
                text=text,
                fill=(0, 0, 0),
                font=self.font_bold,
            )

        # Script
        for n, line in enumerate(lines):
            script_y_start = (len(meta.items()) + 1) * (
                BIG_FONT_SIZE + LINE_HEIGHT
            ) + SCRIPT_MARGIN_TOP
            line_height = (NORMAL_FONT_SIZE + LINE_HEIGHT) * n
            y = script_y_start + line_height
            draw.text(
                (SCRIPT_PADDING, y),
                text=line,
                fill=(0, 0, 0),
                font=self.font_normal,
            )
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()
        return img_byte_arr
