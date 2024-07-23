from peewee import Model, CharField, ForeignKeyField
from app.database import database

class ApiUser(Model):
    name = CharField()
    email = CharField(unique=True)
    password = CharField()

    class Meta:
        database = database

class Location(Model):
    name = CharField()

    class Meta:
        database = database

class Device(Model):
    name = CharField()
    type = CharField()
    login = CharField()
    password = CharField()
    location = ForeignKeyField(Location, backref='devices')
    api_user = ForeignKeyField(ApiUser, backref='devices')

    class Meta:
        database = database