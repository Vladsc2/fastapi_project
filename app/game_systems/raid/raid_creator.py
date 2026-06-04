from game_data.templates.raid import AbstractRaidGS
from game_data.templates.room import RoomGS
from app.schemas.room import RoomMeshSchema
import random
from tools.math import randint_beta, randfloat_beta
from game_data import const
from app.game_systems.raid.get_rooms import get_room_files
from tools.pars import importer


async def form_raid_mesh(raid_gs: AbstractRaidGS) -> list[list[RoomMeshSchema]]:
    number_mesh: list[int] = await _get_raid_number_mesh(raid_gs)

    mesh, rooms_count = await _get_raid_room_mesh(number_mesh)

    await _fill_raid_other_rooms(mesh, rooms_count, raid_gs)

    file_dict: dict[str, list[str]] = await get_room_files(raid_gs.raid_dir)

    await _fill_rooms_links_to_files(mesh, file_dict)

    return mesh


async def rooms_to_dict(raid_mesh: list[list[RoomMeshSchema]]) -> list[list[dict]]:
    return [[room.model_dump() for room in row] for row in raid_mesh]


async def _get_raid_number_mesh(raid_gs: AbstractRaidGS) -> list[int]:
    lines_count = randint_beta(raid_gs.min_lines, raid_gs.max_lines, raid_gs.mode_lines)

    lines = []

    for _ in range( lines_count ):
        lines.append( randint_beta(raid_gs.min_rooms, raid_gs.max_rooms, raid_gs.mode_rooms) )

    return lines



async def _get_raid_room_mesh(number_mesh: list[int]) -> tuple[list[list[RoomMeshSchema]], int]:
    room_counter = 0

    mesh = []

    for room_count in number_mesh:
        room_counter += room_count

        line_list = []
        for _ in range(room_count):
            line_list.append( RoomMeshSchema() )
        mesh.append( line_list )

    return mesh, room_counter



async def _fill_raid_other_rooms(
        mesh: list[list[RoomMeshSchema]],
        room_count: int,
        raid_gs: AbstractRaidGS,
):
    # Определяем процент заполненности комнатами, а не шанс выпадения
    room_loot_percent = randfloat_beta(
        low=raid_gs.room_loot_min_percent,
        high=raid_gs.room_loot_max_percent,
        mode=raid_gs.room_loot_mode_percent,
    )
    room_battle_loot_percent = randfloat_beta(
        low=raid_gs.room_battle_loot_min_percent,
        high=raid_gs.room_battle_loot_max_percent,
        mode=raid_gs.room_battle_loot_mode_percent,
    )
    room_treasure_percent = randfloat_beta(
        low=raid_gs.room_treasure_min_percent,
        high=raid_gs.room_treasure_max_percent,
        mode=raid_gs.room_treasure_mode_percent,
    )
    room_skill_check_percent = randfloat_beta(
        low=raid_gs.room_skill_check_min_percent,
        high=raid_gs.room_skill_check_max_percent,
        mode=raid_gs.room_skill_check_mode_percent,
    )


    one_room_percent = 100 / room_count

    loot_rooms = int( room_loot_percent // one_room_percent )
    battle_loot_rooms = int( room_battle_loot_percent // one_room_percent )
    treasure_rooms = int( room_treasure_percent // one_room_percent )
    skill_check_rooms = int( room_skill_check_percent // one_room_percent )

    await _distribute_room_types(
        mesh=mesh,
        room_count=room_count,
        loot_rooms=loot_rooms,
        battle_loot_rooms=battle_loot_rooms,
        treasure_rooms=treasure_rooms,
        skill_check_rooms=skill_check_rooms,
    )




async def _distribute_room_types(
    mesh: list[list[RoomMeshSchema]],
    room_count: int,
    loot_rooms: int,
    battle_loot_rooms: int,
    treasure_rooms: int,
    skill_check_rooms: int,
) -> None:
    # Собираем все координаты комнат (i, j) на карте
    coords = [(i, j) for i, row in enumerate(mesh) for j, _ in enumerate(row)]

    # Случайно перемешиваем порядок координат
    random.shuffle(coords)

    # Индекс для прохода по перемешанному списку
    idx = 0

    # Функция-помощник для назначения типа группе комнат
    def assign_type(count: int, room_type: str):
        nonlocal idx
        for _ in range(count):
            i, j = coords[idx]
            mesh[i][j].room_type = room_type
            idx += 1
            if idx >= room_count:
                idx = 0


    room_counts = [
        loot_rooms,
        battle_loot_rooms,
        treasure_rooms,
        skill_check_rooms,
    ]
    room_types = [
        const.RoomTypes.LOOT,
        const.RoomTypes.BATTLE_LOOT,
        const.RoomTypes.TREASURE,
        const.RoomTypes.SKILL_CHECK,
    ]

    for count, room_type in zip(room_counts, room_types):
        assign_type(
            count=count,
            room_type=room_type,
        )




async def _fill_rooms_links_to_files(
        mesh: list[list[RoomMeshSchema]],
        file_dict: dict[str, list[str]],
) -> None:

    used_files = {
        const.RoomTypes.BATTLE: [],
        const.RoomTypes.LOOT: [],
        const.RoomTypes.BATTLE_LOOT: [],
        const.RoomTypes.TREASURE: [],
        const.RoomTypes.SKILL_CHECK: [],
    }

    for line in mesh:

        for room in line:

            files = file_dict.get( room.room_type )
            if files is None:
                continue

            file_path = files.pop(0)
            used_files[room.room_type].append( file_path )

            cls_name: str = await importer.get_first_cls_name(file_path)
            cls: RoomGS = await importer.import_class(file_path, cls_name)

            room.room_path = file_path
            room.name = cls.name

            if len( files ) == 0:
                file_dict[room.room_type] = [file for file in used_files[room.room_type]]
                used_files[room.room_type].clear()

