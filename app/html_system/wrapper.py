from app.html_system.format import format_all_lines as __format_all_lines
from app.html_system.format import wrap_html as __wrap_html


async def wrap_pure(text: str) -> str:
    return await _wrap_text(
        text=text,
    )


async def wrap_world(text: str) -> str:
    return await _wrap_text(
        text=text,
    )



async def _wrap_text(
        text: str,
) -> str:
    if not isinstance(text, str):
        raise TypeError(
            f"To wrap 'text' obj, text must be str. Not {type(text)}"
        )

    text: str = await __format_all_lines( text )
    text: str = await __wrap_html( text )

    return text



