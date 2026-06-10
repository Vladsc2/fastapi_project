from app.models.game import MobModel
from game_data import const

class BaseScript():
    _category = "script"

    _meta: dict

    def _form_script_meta(self, game_model, owner, enemies):
        self._meta = {
            self.Meta.GAME_MODEL: game_model,
            self.Meta.ROOM_MODEL: game_model.room,
            self.Meta.PLAYER_CHAR: game_model.character,
            self.Meta.OWNER: owner,
            self.Meta.ENEMIES: enemies,
            self.Meta.IS_MOB: isinstance(owner, MobModel),
        }


    def meta(self, meta_const: int, default=None):
        return self._meta.get(meta_const, default)


    class Meta:
        GAME_MODEL = 0
        ROOM_MODEL = 1
        PLAYER_CHAR = 2
        OWNER = 3
        ENEMIES = 5
        IS_MOB = 6


    # override
    id: str
    trigger: str = const.NONE_CONST
    only_one: bool = True

    async def run(self):
        pass



class SystemScript( BaseScript ):
    _category = BaseScript._category + "/system"


class EnemyScript( BaseScript ):
    _category = BaseScript._category + "/enemy"


class PlayerScript( BaseScript ):
    _category = BaseScript._category + "/player"