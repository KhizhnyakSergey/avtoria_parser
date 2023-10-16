import re
from typing import Optional

from bs4 import BeautifulSoup


class AutoRiaParser:
    
    def __init__(self, html: str) -> None:
        self._soup = BeautifulSoup(html, 'lxml')

    @property
    def seller_username(self) -> Optional[str]:
        tag = self._soup.select_one('.seller_info_name')
        return tag.get_text(strip=True) if tag else None

    @property
    def image_count(self) -> Optional[int]:
        tag = self._soup.select_one('.show-all.link-dotted')
        count = None
        if tag:
            tag = tag.get_text(strip=True)
            count = re.search(r"\d+", tag)
        return int(count.group()) if count else None

    @property
    def car_number(self) -> Optional[str]:
        tag = self._soup.select_one('.state-num')
        number = None
        if tag:
            number = re.search(r"(?<=\>).*(?= \<)", str(tag))
        return number.group().strip() if number else None

    @property
    def car_vin(self) -> Optional[str]:
        tag = self._soup.select_one('span.vin-code')
        if not tag: 
            tag = self._soup.select_one('span.label-vin')
        return tag.get_text(strip=True) if tag else None