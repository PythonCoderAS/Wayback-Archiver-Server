from datetime import datetime

from tortoise import Model
from tortoise.fields import (CharField, DatetimeField, ForeignKeyField, ForeignKeyRelation, IntField, ReverseRelation,
                             TextField)


class Host(Model):
    id: int = IntField(pk=True)
    hostname: str = CharField(256, null=False)
    created_on: datetime = DatetimeField(null=False, auto_now_add=True)

    sessions: ReverseRelation["Session"]


class Session(Model):
    id: int = IntField(pk=True)
    host: ForeignKeyRelation[Host] = ForeignKeyField("models.Host", related_name="sessions", on_delete="CASCADE",
                                                     index=True, null=False)
    created_on: datetime = DatetimeField(null=False, auto_now_add=True)

    host_id: int
    items: ReverseRelation["SessionItem"]


class SessionItem(Model):
    id: int = IntField(pk=True)
    session: ForeignKeyRelation[Session] = ForeignKeyField("models.Session", related_name="items", on_delete="CASCADE",
                                                           index=True)
    session_id: int
    created_on: datetime = DatetimeField(null=False, auto_now_add=True)
    url: str = TextField(null=False)
