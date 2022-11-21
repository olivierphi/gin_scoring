from sqlalchemy.orm import DeclarativeBase

# from sqlalchemy.orm import registry

# from . import aliases


class Base(DeclarativeBase):
    pass
    # registry = registry(
    #     type_annotation_map={
    #         aliases.str_50: String(50),
    #     }
    # )
