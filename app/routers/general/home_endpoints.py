from fastapi import APIRouter, Query, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db_interface import db_interface
from app.cruds.general import profile_crud
from app.models.general import IpAssociationsModel
from app.text_system.general import get_home_text
from app.html_system import wrapper


router = APIRouter(prefix="", tags=["Home"])


@router.get("/", response_class=HTMLResponse)
async def get_home_page(
        request: Request,
        session: AsyncSession = Depends(db_interface.get_session),
) -> str:

    base_url = request.base_url
    client_ip = request.client.host

    ip_association: IpAssociationsModel | None = await profile_crud.get_ip_association(
        ip_address=client_ip,
        raise_if_none=False,
        session=session,
    )

    text = get_home_text(
        base_url=base_url,
        ip_association=ip_association
    )

    text = await wrapper.wrap_pure(
        text=text
    )

    return text
    
