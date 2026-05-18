from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)


class ApiResponse[T](BaseModel):
    data: T | None = None
    success: bool = False
    error_code: int | None = None
    message_list: list[str] | None = None
