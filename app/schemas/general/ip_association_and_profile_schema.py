from app.schemas.base import BaseSchema
from app.schemas.general.ip_association_schema import IpAssociationSchema
from app.schemas.general.profile_schema import ProfileOutputSchema

class IpAssociationAndProfileSchema( BaseSchema ):
    ip_association: IpAssociationSchema
    profile: ProfileOutputSchema | None