from datetime import datetime, timedelta
from enum import Enum

from peewee import Model, IntegerField, AutoField, CharField, DateTimeField

from database.connection import db_inst

class CodeStatus(Enum):
    PENDING = 0
    USED = 1
    EXPIRED = 2

class VerificationCode(Model):
    class Meta:
        database = db_inst
        table_name = "verification_codes"

    id = AutoField(primary_key=True)
    email = CharField(max_length=120,index=True)
    code = CharField(max_length=10)
    created_at = DateTimeField(default=datetime.now)
    expires_at:datetime = DateTimeField(default= lambda: datetime.now() + timedelta(minutes=5))
    status = IntegerField(default=CodeStatus.PENDING.value)

    @classmethod
    def create(cls, **query):
        return super().create(**query)

    def is_expired(self):
        return self.expires_at < datetime.now()

    def is_used(self):
        return self.status == CodeStatus.USED.value

    def is_pending(self):
        return self.status == CodeStatus.PENDING.value