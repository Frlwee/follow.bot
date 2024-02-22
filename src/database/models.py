from tortoise import fields, models


class BaseModel(models.Model):
    id = fields.IntField(pk=True)


class Group(BaseModel):
    name = fields.TextField(max_length=255)
    screen_name = fields.TextField(max_length=255)
    add_by = fields.TextField(max_length=255)
