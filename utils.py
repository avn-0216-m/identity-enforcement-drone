import re

def scrape_drone_id(string: str) -> int:
    try:
        return re.search(r"\d{4}", message.author.display_name).group()
    except AttributeError:
        return None
