import re

def extract_hashtags(text):
    """Extracts all hashtags from a string and returns them in a list."""
    hashtags = re.findall(r'#(\w+)', text)
    return hashtags