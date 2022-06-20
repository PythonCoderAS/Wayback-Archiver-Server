from tortoise import Model
from tortoise.fields import (CharField, DatetimeField, ForeignKeyField, IntField, ReverseRelation, TextField)


class Host(Model):
    id = IntField(pk=True)
    hostname = CharField(256, null=False)
    created_on = DatetimeField(null=False, auto_now_add=True)

    sessions: ReverseRelation["Session"]


class Session(Model):
    id = IntField(pk=True)
    host = ForeignKeyField("models.Host", related_name="sessions", on_delete="CASCADE", index=True, null=False)
    created_on = DatetimeField(null=False, auto_now_add=True)

    items: ReverseRelation["SessionItem"]


class SessionItem(Model):
    id = IntField(pk=True)
    session = ForeignKeyField("models.Session", related_name="items", on_delete="CASCADE", index=True)
    created_on = DatetimeField(null=False, auto_now_add=True)
    url = TextField(null=False)
