from tortoise import fields
from tortoise.models import Model

class User(Model):
    id = fields.IntField(pk = True)
    name = fields.CharField(max_length = 50, null = False)
    lastname = fields.CharField(max_length = 50)
    age = fields.IntField()
    location = fields.CharField(max_length = 100)
    contact = fields.CharField(max_length = 20)
    created_at = fields.DatetimeField(auto_now_add = True)

    class Meta:
        table = "Water_bot_users"