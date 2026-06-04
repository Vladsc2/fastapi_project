from fastapi import HTTPException, status
from game_data import const
import os
from random import shuffle


async def get_room_files(
        raid_dir: str,
) -> dict[str, list[str]]:

    if not os.path.isdir( raid_dir ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Директория рейда по пути '{raid_dir}' не найдена"
        )

    rooms_path = os.path.join(raid_dir, "rooms")

    if not os.path.isdir( rooms_path ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Директория комнат по пути '{rooms_path}' не найдена"
        )


    room_types = [
        const.RoomTypes.BATTLE,
        const.RoomTypes.LOOT,
        const.RoomTypes.BATTLE_LOOT,
        const.RoomTypes.TREASURE,
        const.RoomTypes.SKILL_CHECK,
    ]
    room_dirs = [
        os.path.join( rooms_path, "battle" ),
        os.path.join( rooms_path, "loot" ),
        os.path.join( rooms_path, "battle_loot" ),
        os.path.join( rooms_path, "treasure" ),
        os.path.join( rooms_path, "skill_check" ),
    ]

    file_dict = {}

    for room_type, room_dir in zip(room_types, room_dirs):
        files: list[str] = await _get_files(room_dir)
        if len(files) > 0:
            shuffle( files )
            file_dict[room_type] = files

    return file_dict




async def _get_files(
        dir_path: str,
) -> list[str]:
    if not os.path.isdir( dir_path ):
        return []

    files = []

    for file in os.listdir( dir_path ):
        if not file.endswith(".py"):
            continue
        if file == "__init__.py":
            continue

        files.append( os.path.join(dir_path, file) )


    return files