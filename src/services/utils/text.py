def clear(text):
    if not text:
        return None
    return text.replace('\n', ' ').replace('\r', ' ').replace('\"', '').replace('\'', '')
