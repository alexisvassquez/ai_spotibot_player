USE_EMOJIS = True
USE_SYMBOLS = True

def say(text, emoji=""):
    # Replace text symbols with Unicode-safe glyphs
    if USE_SYMBOLS:
        text = text.replace("->", "\u2191")
        text = text.replace("=>", "\u21D2")
        text = text.replace("<-", "\u2190")

    if USE_EMOJIS and emoji:
        print(f"{emoji} {text}")
    else:
        print(text)
