from peewee import *

db = MySQLDatabase('dwcongress', user='root', passwd='')


class BaseModel(Model):
    class Meta:
        database = db


class Congress(BaseModel):
    idcongress = PrimaryKeyField()
    congressname = CharField()


class Year(BaseModel):
    idyear = PrimaryKeyField()
    congressyear = IntegerField()


class Autor(BaseModel):
    idautor = PrimaryKeyField()
    autorname = CharField()
    workplace = CharField()


class Admissions(BaseModel):
    idadmcongress = PrimaryKeyField()
    idadmautor = IntegerField()
    accepted = IntegerField()
    refused = IntegerField()
    idadmyear = IntegerField()



