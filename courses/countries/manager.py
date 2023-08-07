from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

import courses.countries.exceptions as exceptions
from courses.countries.db_adapter import SQLAlchemyCountriesAdapter
from courses.countries.schemas import CountryRead, CountryBlockRead, CountryBlockCreate, CountryCreate, CountryUpdate, \
    CountryBlockUpdate


class CountriesManager:
    def __init__(self,
                 session: AsyncSession
                 ):
        self.db_adapter = SQLAlchemyCountriesAdapter(session=session)

    async def get_countries(
            self,
            country_block_id: int
    ) -> List[CountryRead]:
        """
        Get countries with parameters.

        :param country_block_id: A country block id.
        :raises CountriesNotFound: Countries with these parameters has not been found.
        :return: A countries.
        """
        countries = await self.db_adapter.get_countries(country_block_id)

        if not countries:
            raise exceptions.CountriesNotFound()
        return countries

    async def get_country_blocks(
            self
    ) -> List[CountryBlockRead]:
        """
        Get country blocks.

        :return: Country blocks.
        """
        country_blocks = await self.db_adapter.get_country_blocks()
        return country_blocks

    async def create_country(
            self,
            country_create: CountryCreate
    ) -> CountryRead:
        """
        Create a country in database.

        :param country_create: The CountryCreate model to create.
        :return: A new country.
        """
        country_dict = country_create.create_update_dict()

        created_country = await self.db_adapter.create_country(country_dict)
        return created_country

    async def create_country_block(
            self,
            country_block_create: CountryBlockCreate
    ) -> CountryBlockRead:
        """
        Create a country block in database.

        :param country_block_create: The CountryBlockCreate model to create.
        :return: A new country block.
        """
        country_block_dict = country_block_create.create_update_dict()

        created_country_block = await self.db_adapter.create_country_block(country_block_dict)
        return created_country_block

    async def update_country(
            self,
            country_id: int,
            country_update: CountryUpdate
    ) -> CountryRead:
        """
        Update a country in database.

        :param country_id: A country id.
        :param country_update: The CountryUpdate model to update.
        :raises CountryNotExist: A country with this id is not exist.
        :return: An updated country.
        """
        country = await self.db_adapter.get_country(country_id)
        if country is None:
            raise exceptions.CountryNotExist
        country_dict = country_update.create_update_dict()

        updated_country = await self.db_adapter.update_country(country, country_dict)
        return updated_country

    async def update_country_block(
            self,
            country_block_id: int,
            country_block_update: CountryBlockUpdate
    ) -> CountryBlockRead:
        """
        Update a country block in database.

        :param country_block_id: A country block id.
        :param country_block_update: The CountryBlockUpdate model to update.
        :raises CountryBlockNotExist: A country block with this id is not exist.
        :return: An updated country block.
        """
        country_block = await self.db_adapter.get_country_block(country_block_id)
        if country_block is None:
            raise exceptions.CountryBlockNotExist
        country_block_dict = country_block_update.create_update_dict()

        updated_country_block = await self.db_adapter.update_country_block(country_block, country_block_dict)
        return updated_country_block

    async def delete_country(
            self,
            country_id: int
    ) -> None:
        """
        Delete a country in database.

        :param country_id: The id of the country to delete.
        :raises CountryNotExist: A country with this id is not exist.
        """
        country = await self.db_adapter.get_country(country_id)
        if country is None:
            raise exceptions.CountryNotExist

        await self.db_adapter.delete_country(country)

    async def delete_country_block(
            self,
            country_block_id: int
    ) -> None:
        """
        Delete a country block in database.

        :param country_block_id: The id of the country block to delete.
        :raises CountryBlockNotExist: A country block with this id is not exist.
        """
        country_block = await self.db_adapter.get_country_block(country_block_id)
        if country_block is None:
            raise exceptions.CountryBlockNotExist

        await self.db_adapter.delete_country_block(country_block)
