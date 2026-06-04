from game_data.templates.effect import BaseEffect, TickEffect
from game_data.templates.damage_formula import Damage
from game_data import const
from app.models.game import GameModel
from app.models.game import BaseCharacterModel, MobModel
from app.game_systems.roll import roll4
from app.game_systems.character import entity_health

class Poison( TickEffect ):
    id = "poison"
    event = const.Event.END_TURN

    alignment = TickEffect.Alignment.NEGATIVE
    updatable = True

    name = "Отравление"
    desc = "В конце хода наносит 1d4 урона ядом"

    save_throw_stat = const.Stat.Constitution
    save_throw_diff = 20



    def tick(self) -> str:
        game_model: GameModel = self.meta( self.Meta.GAME_MODEL )
        target: BaseCharacterModel = self.meta( self.Meta.TARGET )

        text = f"Тик эффекта отравление\n"
        value = roll4()
        text += f"  Значение 1d4 = {value}"

        damage = Damage(damage_type=const.DamageType.Exotic.POISON, value=value)

        if isinstance(target, MobModel):
            text += entity_health.entity_take_damage(
                game_model=game_model,
                attacker=None,
                target=target,
                damage=damage
            )

        return text