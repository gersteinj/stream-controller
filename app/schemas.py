from pydantic import BaseModel

class Robot(BaseModel):
    # Making this int or none allows for not providing an id value
    # ID value is auto-generated by ORM
    # Not sure if this is the best way to do it.
    id: int | None
    display_name: str
    name: str | None
    weight_class: str

    class Config:
        orm_mode = True
        