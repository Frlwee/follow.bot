from typing import ClassVar, Any

from pydantic import BaseModel


class __BaseEvent(BaseModel):
    __separator__: ClassVar[str] = ":"

    # Предполагается использование этого кода для упаковки
    # и распаковки данных в строковом формате. (like aiogram style)
    # Но в силу того, что ВК требует JSON (as string), этот код (пока) не используется.

    @property
    def __prefix__(self) -> str:
        return self.__class__.__name__

    def __encode_value(self, value: Any) -> str:
        serialized = self.Config.json_dumps(value, default=self.__json_encoder__)
        deserialized = self.Config.json_loads(serialized)

        if deserialized is None:
            return ""

        return str(deserialized)

    def pack(self):
        result = [self.__prefix__]

        for key, value in self.dict().items():
            encoded = self.__encode_value(value)

            if self.__separator__ in encoded:
                raise ValueError(
                    f"Separator {self.__separator__!r} can not be used in value"
                    f"{key}={encoded!r}"
                )

            result.append(encoded)

        return self.__separator__.join(result)

    @classmethod
    def unpack(cls, value: str):
        schema, payload = cls.schema(), {}
        prefix, *arguments = value.split(cls.__separator__)
        properties, required = schema.get("properties"), schema.get("required")

        if prefix != cls.__name__:
            raise ValueError(
                f"Incorrect prefix given  ({prefix!r} != {cls.__prefix__!r}), "
            )

        if len(arguments) != len(properties):
            raise TypeError(
                f"{cls.__name__!r} takes {len(arguments)} arguments, "
                f"but were given {len(properties)}"
            )

        for name, value in zip(list(properties.keys()), arguments):
            if value == "" and name not in required:
                value = None
            payload[name] = value

        return cls(**payload)


class BaseEvent(BaseModel):
    def pack(self):
        return self.json()
