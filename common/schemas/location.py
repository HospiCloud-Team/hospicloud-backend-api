from pydantic import BaseModel
from enum import Enum

from pydantic.types import constr


class Province(str, Enum):
    azua = "azua"
    bahoruco = "bahoruco"
    barahona = "barahona"
    dajabon = "dajabon"
    distrito_nacional = "distrito_nacional"
    duarte = "duarte"
    elias_pina = "elias_pina"
    el_seibo = "el_seibo"
    espaillat = "espaillat"
    hato_mayor = "hato_mayor"
    hermanas_mirabal = "hermanas_mirabal"
    independencia = "independencia"
    la_altagracia = "la_altagracia"
    la_romana = "la_romana"
    la_vega = "la_vega"
    maria_trinidad_sanchez = "maria_trinidad_sanchez"
    monsenor_nouel = "monsenor_nouel"
    monte_cristi = "monte_cristi"
    monte_plata = "monte_plata"
    pedernales = "pedernales"
    peravia = "peravia"
    puerto_plata = "puerto_plata"
    samana = "samana"
    sanchez_ramirez = "sanchez_ramirez"
    san_cristobal = "san_cristobal"
    san_jose_de_ocoa = "san_jose_de_ocoa"
    san_juan = "san_juan"
    san_pedro_de_macoris = "san_pedro_de_macoris"
    santiago = "santiago"
    santiago_rodriguez = "santiago_rodriguez"
    santo_domingo = "santo_domingo"
    valverde = "valverde"


class LocationBase(BaseModel):
    address: constr(strip_whitespace=True)
    province: Province


class LocationIn(LocationBase):
    pass


class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True
