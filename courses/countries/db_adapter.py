from typing import Any, Dict, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from base_db_adapter import base_get, base_create_update
from models import Country, CountryBlock


class SQLAlchemyCountriesAdapter:
    session: AsyncSession

    def __init__(self,
                 session: AsyncSession,
                 ):
        self.session = session

    async def get_country(self, country_id: int) -> Country:
        statement = select(Country).where(Country.id == country_id)
        return await base_get(self.session, statement)

    async def get_countries(self, country_block_id: int) -> List[Country]:
        statement = select(Country).where(Country.country_block_id == country_block_id).order_by(Country.name)
        return await base_get(self.session, statement, one_scalar=False)

    async def get_country_block(self, country_block_id: int) -> CountryBlock:
        statement = select(CountryBlock).where(CountryBlock.id == country_block_id)
        return await base_get(self.session, statement)

    async def get_country_blocks(self) -> List[CountryBlock]:
        statement = select(CountryBlock)
        return await base_get(self.session, statement, one_scalar=False)

    async def create_country(self, country_dict: Dict[str, Any]) -> Country:
        country = Country(**country_dict)
        await base_create_update(self.session, country)

        country = await self.get_country(country.id)
        return country

    async def create_country_block(self, country_block_dict: Dict[str, Any]) -> CountryBlock:
        country_block = CountryBlock(**country_block_dict)
        await base_create_update(self.session, country_block)

        country_block = await self.get_country_block(country_block.id)
        return country_block

    async def update_country(self, update_country: Country, update_dict: Dict[str, Any]) -> Country:
        for key, value in update_dict.items():
            if value is None:
                continue
            setattr(update_country, key, value)
        await base_create_update(self.session, update_country)

        country = await self.get_country(update_country.id)
        return country

    async def update_country_block(self, update_country_block: CountryBlock, update_dict: Dict[str, Any]) -> CountryBlock:
        for key, value in update_dict.items():
            if value is None:
                continue
            setattr(update_country_block, key, value)
        await base_create_update(self.session, update_country_block)

        country_block = await self.get_country_block(update_country_block.id)
        return country_block

    async def delete_country(self, country: Country) -> None:
        await self.session.delete(country)
        await self.session.commit()

    async def delete_country_block(self, country_block: CountryBlock) -> None:
        await self.session.delete(country_block)
        await self.session.commit()
