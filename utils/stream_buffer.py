# utils/stream_buffer.py

class StreamBuffer:
    def __init__(self):
        self.tokens = []

    def feed(self, token: str):
        """接收新 token（通常来自 LLM 的 delta.content）"""
        self.tokens.append(token)

    def preview(self) -> str:
        """返回当前所有内容（实时回显）"""
        return "".join(self.tokens)

    def get_full_text(self) -> str:
        """返回最终完整内容"""
        return self.preview()

    def reset(self):
        """清空缓存"""
        self.tokens = []
