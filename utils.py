import re
from typing import List
import urllib.request
from urllib.error import HTTPError, URLError


def extract_logs(urls: str):
    content = []
    urls = [url.strip() for url in urls.split(",")]
    for url in urls:
        try:
            resp = urllib.request.urlopen(url)
            text = resp.read().decode("utf-8")

            # Remove timestamps (e.g., '00:01:11,430 --> 00:01:40,520')
            try:
                text = re.sub(
                    r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", "", text
                )
            except re.error:
                pass
            # Remove line numbers
            try:
                text = re.sub(r"\d+", "", text)
            except re.error:
                pass

            # Replace PC style carriage return with unix style new line
            text = re.sub("(\r\n)+|(\n{2,})", "\n", text)

            content.append(text.strip())

        except (ValueError, URLError, HTTPError) as e:
            pass
    return "\n".join(content)
