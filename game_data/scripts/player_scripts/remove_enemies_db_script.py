from app.models.room import RoomModel
from app.models.game import MobModel
from game_data.templates.script import PlayerScript
from app.game_systems.room.tools import state_manager
from game_data import const

class RemoveEnemiesDBScript( PlayerScript ):

    id = "remove_enemies_db"
    trigger = const.Trigger.CLOSE_BATTLE
    only_one = False

    async def run(self):
        room_model: RoomModel = self.meta( self.Meta.ROOM_MODEL )
        if len(room_model.enemies) == 0:
            return

        # Помечаем всех энтити на удаление
        entities: list[MobModel] = self.meta( self.Meta.ENEMIES )
        for mob_model in entities:
            mob_model._delete_label = True

        # Удаляем ссылки на entity по id
        is_int = isinstance(room_model.enemies[0], int)

        if is_int:
            room_model.enemies = []
        else:
            encounter_ptr = state_manager.get_state_value(room_model, const.RoomStates.General.INIT) - 1
            # Отнимаем 2 раза потому что
            # 1) Мы получаем увеличенное число - прошлое состояние. То есть в первой итерации INIT: 2
            # 2) Чтобы привести к индексу
            room_model.enemies[ encounter_ptr-1 ] = []

