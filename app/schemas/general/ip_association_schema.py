from app.schemas.base import BaseSchema

class IpAssociationSchema( BaseSchema ):

    ip_address: str
    profile_id: int | None


    def __repr__(self):
        return f"{self.__class__.__name__}(ip_address={self.ip_address}, profile_id={self.profile_id})"

