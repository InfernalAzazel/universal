class CreateI18n:
    def __init__(self, locale: str, messages: dict):
        if locale not in messages:
            raise ValueError(f"Locale '{locale}' not found in messages")

        self.locale = locale
        self.messages = messages

    def t(self, key) -> str:
        return self.messages[self.locale].get(key, key)
