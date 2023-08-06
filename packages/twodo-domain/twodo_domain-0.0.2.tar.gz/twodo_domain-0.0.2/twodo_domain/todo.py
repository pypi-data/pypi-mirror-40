import datetime
import typing as t
from dataclasses import dataclass


from twodo_domain.person import Person


@dataclass
class Item:

    name: str
    description: str
    created_at: datetime.datetime


@dataclass
class ToDo:

    name: str
    comment: str
    creator: Person
    created_at: datetime.datetime
    items: t.List
