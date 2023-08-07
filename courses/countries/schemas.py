from typing import List

from pydantic import BaseModel

from base_schema import CreateUpdateDictMixin


class BaseCountry(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CountryRead(BaseCountry):
    id: int
    pass


class CountryCreate(BaseCountry, CreateUpdateDictMixin):
    country_block_id: int
    pass


class CountryUpdate(BaseCountry, CreateUpdateDictMixin):
    name: str | None
    country_block_id: int | None



class BaseCountryBlock(BaseModel):
    name: str

    class Config:
        orm_mode = True


class CountryBlockRead(BaseCountryBlock):
    id: int
    countries: List["CountryRead"]
    pass


class CountryBlockCreate(BaseCountryBlock, CreateUpdateDictMixin):
    pass


class CountryBlockUpdate(BaseCountryBlock, CreateUpdateDictMixin):
    name: str | None
