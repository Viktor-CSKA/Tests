"""Контракты ответов API. Лишние или пропавшие поля и неверные типы роняют тест."""

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class Post(StrictModel):
    userId: int = Field(gt=0)
    id: int = Field(gt=0)
    title: str = Field(min_length=1)
    body: str = Field(min_length=1)


class Comment(StrictModel):
    postId: int = Field(gt=0)
    id: int = Field(gt=0)
    name: str
    email: EmailStr
    body: str


class Geo(StrictModel):
    lat: str
    lng: str


class Address(StrictModel):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


class Company(StrictModel):
    name: str
    catchPhrase: str
    bs: str


class User(StrictModel):
    id: int = Field(gt=0)
    name: str
    username: str
    email: EmailStr
    address: Address
    phone: str
    website: str
    company: Company


class Todo(StrictModel):
    userId: int = Field(gt=0)
    id: int = Field(gt=0)
    title: str
    completed: bool
