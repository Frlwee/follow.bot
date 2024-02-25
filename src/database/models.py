from tortoise import fields, models, Tortoise
from tortoise.functions import Sum


class BaseModel(models.Model):
    id = fields.IntField(pk=True)

    @classmethod
    async def sum(cls, field_name: str, **filter_kwargs) -> float:
        annotate_key = f"{field_name}_sum"
        query = (
            await cls.filter(**filter_kwargs)
            .annotate(**{annotate_key: Sum(field_name)})
            .first()
            .values(annotate_key)
        )
        return query[annotate_key] or 0.0

    class Meta:
        abstract = True

    class PydanticMeta:
        exclude_raw_fields = True
        max_recursion = 15


class CreatedAtMixin:
    created_at = fields.DatetimeField(auto_now_add=True)


class Group(BaseModel):
    name = fields.TextField(max_length=255)
    screen_name = fields.TextField(max_length=255)
    add_by = fields.TextField(max_length=255)


Tortoise.init_models(["src.database.models"], "models")
