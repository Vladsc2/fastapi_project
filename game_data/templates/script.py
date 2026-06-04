

class BaseScript():
    _category = "script"

    _meta = {}

    META_PLAYER_CHAR = 0
    META_ENTITY = 1
    META_ATTACKER = 2
    META_DAMAGE = 3
    META_GAME_MODEL = 4
    META_ROOM_MODEL = 5

    id: str

    def _form_meta(self, game_model, room_model, player_char, entity, attacker, damage):
        self._meta = {
            self.META_GAME_MODEL: game_model,
            self.META_ROOM_MODEL: room_model,
            self.META_PLAYER_CHAR: player_char,
            self.META_ENTITY: entity,
            self.META_ATTACKER: attacker,
            self.META_DAMAGE: damage,
        }


    def get_meta(self, const: int):
        return self._meta.get(const)


    def death_trigger(self):
        pass



class SystemScript( BaseScript ):
    _category = BaseScript._category + "/system"


class EnemyScript( BaseScript ):
    _category = BaseScript._category + "/enemy"


class PlayerScript( BaseScript ):
    _category = BaseScript._category + "/player"