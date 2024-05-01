from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

class CustomBase(MappedAsDataclass, DeclarativeBase):
    """subclasses will be converted to dataclasses"""