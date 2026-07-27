def clean_text(text):
    if text is None:
        return None
    text = text.replace("\xa0", " ")
    text = " ".join(text.split())
    return text.strip()