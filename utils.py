import re
from typing import List
import urllib.request
from urllib.error import HTTPError, URLError


def extract_logs(urls: List[str]) -> str:
    """Consume, clean, and combine urls pointing to log files

    Args:
        urls (List[str]): URLs pointing to logfiles

    Returns:
        str: Combined logs for injection into AI prompt
    """

    content = []
    urls = [url.strip() for url in urls]
    for url in urls:
        try:
            resp = urllib.request.urlopen(url)
            text = resp.read().decode("utf-8")

            # Remove timestamps (e.g., '00:01:11,430 --> 00:01:40,520')
            text = re.sub(
                r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", "", text
            )
            # Remove line numbers
            text = re.sub(r"\d+", "", text)
            # Replace double blank lines (PC style carriage return or unix style) with single unix style new line
            text = re.sub("(\r\n)+|(\n{2,})", "\n", text)

            content.append(text.strip())

        except (ValueError, URLError, HTTPError):
            pass
    return "\n".join(content)
