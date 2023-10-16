import asyncio
from typing import (
    Optional, 
    List, 
    AsyncGenerator, 
    Any, 
    Dict,
)

from src.core.parser import AutoRiaParser
from src.dto.autoria import TicketShort, SellerPhones
from src.dto.converters import convert_data_to_ticket_short, convert_data_to_seller_phones
from src.session.aiohttp import AiohttpSession
from src.core.user_agent import get_user_agent


class AutoRiaAPI:

    API: str = 'https://auto.ria.com'

    def __init__(self, proxy: Optional[str] = None) -> None:
        self._session = AiohttpSession(api=self.API, proxy=proxy)
        self._headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

    async def __aenter__(self) -> "AutoRiaAPI":
        return self
    
    async def __aexit__(self, *args) -> None:
        await self._session.close()

    async def iter_used_car_ids_list(
            self, page: int = 0, limit: int = 100, timeout: Optional[float] = None
    ) -> AsyncGenerator[Any, List[str]]:
        last_page = 99999

        while page < last_page:
            print(f"Collecting data from page -> {page + 1}")
            self._headers['user-agent'] = get_user_agent()

            params = {
                'indexName': 'auto',
                'abroad': '2',
                'custom': '1',
                'page': str(page),
                'countpage': str(limit),
                'with_feedback_form': '1',
                'withOrderAutoInformer': '1',
                'with_last_id': '1',
            }

            response = await self._session(
                'GET', '/api/search/auto', params=params, headers=self._headers
            )

            result = response['result']['search_result']
            ids = result['ids']
            last_page = int(result['count'] / limit)
            yield ids 
            
            page += 1
            if timeout is not None:
                await asyncio.sleep(timeout)

    
    async def get_short_ticket_data(
            self, ticket_id: str, ticket_type: str = 'bu'
    ) -> TicketShort:

        self._headers['user-agent'] = get_user_agent()

        params = {
            'type': ticket_type,
            'langId': '4',
        }

        response = await self._session(
            'GET', f'/demo/bu/mainPage/rotator/item/{ticket_id}', params=params, headers=self._headers
        )

        return convert_data_to_ticket_short(response)
    
    async def get_seller_numbers(self, ticket_id: str, ticket_hash: str, expires: int) -> SellerPhones:
        self._headers['user-agent'] = get_user_agent()

        params = {
            'hash': ticket_hash,
            'expires': str(expires),
        }

        response = await self._session(
            'GET', f'/users/phones/{ticket_id}', params=params, headers=self._headers
        )

        return convert_data_to_seller_phones(response)
    
    async def get_ticket(self, endpoint: str) -> AutoRiaParser:
        self._headers['user-agent'] = get_user_agent()

        response = await self._session(
            'GET', endpoint, headers=self._headers
        )

        return AutoRiaParser(response)