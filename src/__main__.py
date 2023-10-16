import asyncio
import re
import pytz
from typing import List
from datetime import datetime

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.database.core.connection import async_engine, create_session_factory, async_session, pg_dump
from src.database.core.database import Database
from src.dto.ticket import TicketCreate
from src.dto.phone import PhoneCreate
from src.core.app import AutoRiaAPI
from src.dto.autoria import DBData


async def get_all_data(api: AutoRiaAPI, tickets: List[str]) -> List[DBData]:

    async def _task(ticket_id: str) -> DBData:
        short_data = await api.get_short_ticket_data(ticket_id)
        page_data = await api.get_ticket(short_data.link)
        phones = await api.get_seller_numbers(ticket_id, short_data.userSecure.hash, short_data.userSecure.expires)
        odometer = re.search(r"\d+", short_data.race) 
        if odometer:
            odometer = int(odometer.group() + "000")

        return DBData(
            ticket_id=int(ticket_id),
            url=api.API + short_data.link,
            title=f'{short_data.marka} {short_data.model} {short_data.year}',
            price=int(short_data.USD.replace(" ", "")),
            odometer=odometer,
            username=page_data.seller_username,
            phone_numbers=phones.phones,
            image_url=short_data.photoBig,
            images_count=page_data.image_count,
            car_number=page_data.car_number,
            car_vin=page_data.car_vin,
            is_active=True if page_data.seller_username else False,
            found_date=datetime.now(pytz.timezone('Europe/Kyiv'))
        )
    
    tasks = (asyncio.create_task(_task(ticket_id)) for ticket_id in tickets)
    return await asyncio.gather(*tasks)


async def get_actual_data() -> None:

    engine = async_engine()

    async with AutoRiaAPI() as api:
        async for tickets in api.iter_used_car_ids_list(page=21, timeout=3):
            data = await get_all_data(api, tickets)
            async with Database(session=async_session(create_session_factory(engine))) as db:
                tickets = []
                phones = []
                for db_data in data:
                    tickets.append(TicketCreate(
                        ticket_id=db_data.ticket_id,
                        url=db_data.url,
                        title=db_data.title,
                        price=db_data.price,
                        odometer=db_data.odometer,
                        username=db_data.username,
                        image_url=db_data.image_url,
                        images_count=db_data.images_count,
                        car_number=db_data.car_number,
                        car_vin=db_data.car_vin,
                        found_date=db_data.found_date,
                        is_active=db_data.is_active
                    ))
                    for phone in db_data.phone_numbers or []:
                        phones.append(PhoneCreate(
                            phone_number=phone,
                            ticket_id=db_data.ticket_id
                        ))
                await db.ticket.create_many(tickets)
                await db.phone.create_many(phones)
            # break
    await engine.dispose()


async def main():
    sheduler = AsyncIOScheduler()
    timezone = pytz.timezone('Europe/Kyiv')
    trigger = CronTrigger('*', '*', '*', hour=4, minute=24, timezone=timezone)
    trigger_dump = CronTrigger('*', '*', '*', hour=4, minute=27, timezone=timezone)
    sheduler.add_job(get_actual_data, trigger=trigger)
    sheduler.add_job(pg_dump, trigger=trigger_dump)
    sheduler.start()
    while True:
       await asyncio.sleep(3)
   
   


if __name__ == "__main__":
    # asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
    
