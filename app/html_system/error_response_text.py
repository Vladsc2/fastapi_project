from fastapi import HTTPException
from fastapi.responses import HTMLResponse
from app.html_system import wrapper

async def form_error_text(error: HTTPException) -> HTMLResponse:
    error_text = f"CODE: {error.status_code}\n\n{error.detail}"
    error_text = await wrapper.wrap_pure( error_text )

    return HTMLResponse(
        status_code=error.status_code,
        content=error_text,
    )