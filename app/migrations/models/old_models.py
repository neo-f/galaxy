from tortoise import Model, fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class Tag(models.Model):
    name = fields.CharField(max_length=255, description="tag name")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

    class PydanticMeta:
        pass


TagDetail = pydantic_model_creator(Tag, name="Tag")
TagCreate = pydantic_model_creator(Tag, exclude=("id", ...))

MAX_VERSION_LENGTH = 255


class Aerich(Model):
    version = fields.CharField(max_length=MAX_VERSION_LENGTH)
    app = fields.CharField(max_length=20)

    class Meta:
        ordering = ["-id"]
