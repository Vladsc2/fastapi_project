from app.models.game import GameModel
from app.models.game import BaseCharacterModel, MainCharacterModel, MobModel
from game_data.templates.damage_formula import Damage
from game_data import const

from game_data.const import const_modifier
from app.game_systems.character import entity_script

from app.game_systems.battle.round_manager import battle_win

async def entity_take_damage(
        game_model: GameModel,
        attacker: BaseCharacterModel | None,
        target: MobModel,
        damage: Damage,
        enemies: list[MobModel],
) -> str:
    text = ""

    target.hp = target.hp - damage.value
    if target.hp < 0:
        target.hp = 0

    if attacker is not None:
        text += (f"\n{attacker.name} наносит {target.name} {damage.value}"
                 f" {const_modifier.get_readable_genitive_damage_type(damage.damage_type).lower()} урона\n\n")
    else:
        text += (f"\n{target.name} получает {damage.value}"
                 f" {const_modifier.get_readable_genitive_damage_type(damage.damage_type).lower()} урона\n\n")

    if target.hp == 0:
        text += f"{target.name} умер\n\n"

        await entity_script.execute_script_by_trigger(
            game_model=game_model,
            owner=target,
            enemies=enemies,
            trigger=const.Trigger.DEATH,
        )

        battle_win.check_battle_win(
            room_model=game_model.room,
            enemies=enemies,
        )


    return text
