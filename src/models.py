from tortoise import Model
from tortoise.fields import (
    IntField,
    CharField,
    DatetimeField,
    ForeignKeyField, TextField,
)

class Host(Model):
    id = IntField(pk=True)
    hostname = CharField(256, null=False) # Actually the user agent.

class Session(Model):
    id = IntField(pk=True)
    host = ForeignKeyField("Host", related_name="sessions", on_delete="CASCADE", index=True)
    created_on = DatetimeField(null=False, auto_now_add=True)

class SessionItem(Model):
    id = IntField(pk=True)
    session = ForeignKeyField("Session", related_name="items", on_delete="CASCADE", index=True)
    created_on = DatetimeField(null=False, auto_now_add=True)
    url = TextField(null=False)
