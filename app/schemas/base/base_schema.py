from pydantic import BaseModel, ConfigDict


class BaseSchema( BaseModel ):
    model_config = ConfigDict(from_attributes=True)


    def __str__(self):
        return repr( self )


    def __repr__(self):
        return f"{self.__class__.__name__}"