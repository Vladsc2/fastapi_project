from app.models.room import RoomModel
from app.models.game import MobModel
from game_data.templates.script import EnemyScript
from app.game_systems.room.tools import state_manager
from game_data import const

class RemoveFromDBScript( EnemyScript ):

    id = "remove_db"

    def close_battle_trigger(self):
        entity: MobModel = self.get_meta( self.META_ENTITY )
        entity._delete_label = True


        room_model: RoomModel = self.get_meta( self.META_ROOM_MODEL )
        is_int = isinstance(room_model.enemies[0], int)

        if is_int:
            room_model.enemies.remove( entity.id )

        else:
            encounter_ptr = state_manager.get_state_value(room_model, const.RoomStates.General.INIT) - 1
            # Отнимаем 2 раза потому что
            # 1) Мы получаем увеличенное число - прошлое состояние. То есть в первой итерации INIT: 2
            # 2) Чтобы привести к индексу
            # Создаем новый список, так как алхимия не отслеживает состояния внутри вложенных списков
            inner = room_model.enemies[ encounter_ptr-1 ].copy()
            inner.remove( entity.id )
            room_model.enemies[ encounter_ptr-1 ] = inner
