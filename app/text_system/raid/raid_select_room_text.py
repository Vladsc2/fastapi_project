from app.models.room import RoomModel

def get_text(
        room_number: int,
        room_model: RoomModel,
) -> str:

    return f"""
        Вы перешли в локацию '{room_model.name}'
         - room_type = {room_model.room_type}
         - room_path = {room_model.room_path}
         
        <a href="/room">Перейти на страницу локации</a>
    """