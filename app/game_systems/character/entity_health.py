from app.models.game import GameModel
from app.models.game import BaseCharacterModel, MainCharacterModel, MobModel
from game_data.templates.damage_formula import Damage

from game_data.const import const_modifier
from game_data.scripts import scripts_system

from app.game_systems.battle.round_manager import battle_win

def entity_take_damage(
        game_model: GameModel,
        attacker: BaseCharacterModel | None,
        target: MobModel,
        damage: Damage,
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

        _scripts_death_trigger(
            game_model=game_model,
            attacker=attacker,
            entity=target,
            damage=damage
        )

        battle_win.check_battle_win(
            room_model=game_model.room,
        )


    return text



def _scripts_death_trigger(
        game_model: GameModel,
        attacker: BaseCharacterModel | None,
        entity: BaseCharacterModel,
        damage: Damage,
):

    for script_url in entity.scripts:
        script_cls = scripts_system.get_script_by_url(script_url)
        script = script_cls()
        script._form_meta(
            game_model=game_model,
            room_model=game_model.room,
            player_char=game_model.character,
            entity=entity,
            attacker=attacker,
            damage=damage,
        )
        script.death_trigger()