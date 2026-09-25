"""Тестовые данные SauceDemo: пользователи и каталог товаров."""

from dataclasses import dataclass

PASSWORD = "secret_sauce"


class Users:
    STANDARD = "standard_user"
    LOCKED_OUT = "locked_out_user"


@dataclass(frozen=True)
class Product:
    name: str
    price: float

    @property
    def slug(self) -> str:
        """Часть data-test атрибута кнопок: 'Sauce Labs Backpack' -> 'sauce-labs-backpack'."""
        return self.name.lower().replace(" ", "-")


class Products:
    BACKPACK = Product("Sauce Labs Backpack", 29.99)
    BIKE_LIGHT = Product("Sauce Labs Bike Light", 9.99)
    BOLT_T_SHIRT = Product("Sauce Labs Bolt T-Shirt", 15.99)
    FLEECE_JACKET = Product("Sauce Labs Fleece Jacket", 49.99)
    ONESIE = Product("Sauce Labs Onesie", 7.99)

    ALL = (BACKPACK, BIKE_LIGHT, BOLT_T_SHIRT, FLEECE_JACKET, ONESIE)


CATALOG_SIZE = 6
TAX_RATE = 0.08
