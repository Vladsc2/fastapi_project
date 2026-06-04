from app.models import GameModel
from app.models.game import MobModel, BaseCharacterModel
from game_data.templates.effect import (EffectApplication, BaseEffect, TickEffect, StatModifierEffect,
                                        get_stat_modifier_effect_view)
from game_data.effects import effect_system
from app.schemas.effect import EffectSchema
from app.game_systems.roll import roll20
from app.game_systems.character import stat as char_stat
from game_data.const import const_modifier
from game_data import const
from app.text_system import form

"""
    Interfaces
"""

async def add_effect(entity: BaseCharacterModel, caster_id: int | None, effect_app: EffectApplication) -> str:
    return await _add_effect_handle(entity, caster_id, effect_app)



async def get_effects(entity: BaseCharacterModel) -> list[EffectSchema]:
    return await _get_effects(entity)



async def apply_effects_on_entity(game_model: GameModel, entity: MobModel, event: str) -> str:
    return await _apply_effects_on_entity(game_model, entity, event)



"""
    Realization
"""

async def _add_effect_handle(entity: BaseCharacterModel, caster_id: int | None, effect_app: EffectApplication) -> str:
    effect = effect_system.get_effect_by_url(effect_app.url)
    if effect is None:
        print(f"Add Effect Error: Не удалось получить эффект с url {effect_app.url}")
        return ""

    effect_schema = EffectSchema(
        effect_type=effect._effect_type,
        event=effect.event,
        times=effect_app.time,
        caster_id=caster_id,
        effect_url=effect_app.url,
    )

    if effect_schema.effect_type == BaseEffect.Type.TICK_EFFECT:
        return await _add_tick_effect(entity, effect_schema, effect)

    if effect_schema.effect_type == BaseEffect.Type.STAT_MODIFIER:
        return await _add_stat_effect(entity, effect_schema, effect)


    return (f"Необработанный тип эффекта для добавления на character\n\n"
            f" - {__file__}\n"
            f" - effect_type: {effect_schema.effect_type}\n")



async def _add_tick_effect(
        entity: BaseCharacterModel,
        add_effect_schema: EffectSchema,
        effect: TickEffect
) -> str:
    # Проверка, нет ли эффекта с такой же или большей продолжительностью на цели
    effects = await _get_effects(entity)
    if not await _check_add_possibility(effects, add_effect_schema, effect):
        return f"Эффект '{effect.name}' большей или такой же продолжительностью уже наложен на цель\n\n"


    text = f"Накладывание эффекта '{effect.name}'\n"
    # Спасбросок, если нужно
    if effect.save_throw_stat is not None:
        text += f"  Спасбросок {const_modifier.get_readable_genitive_stat(effect.save_throw_stat).lower()}\n"
        text += f"  Сложность: {effect.save_throw_diff}\n"
        roll_value = roll20()
        modifier = char_stat.get_stat_modifier(entity, effect.save_throw_stat)
        text += f"  Значение броска: {roll_value}\n"
        save_throw_value = roll_value + modifier
        if modifier != 0:
            text += f"  Модификатор характеристики: {modifier}\n"
            if save_throw_value >= effect.save_throw_diff:
                text += f"  {roll_value} + {modifier} = {save_throw_value}  >  {effect.save_throw_diff}\n"
            else:
                text += f"  {roll_value} + {modifier} = {save_throw_value}  <  {effect.save_throw_diff}\n"

        if save_throw_value >= effect.save_throw_diff:
            text += f"  Спасбросок успешен\n"
            return text
        else:
            text += f"  Спасбросок провален\n"

    await _add_effect_to_entity(
        entity=entity,
        effects=effects,
        effect_schema=add_effect_schema,
        effect=effect
    )

    text += (f"Эффект '{effect.name}' наложен на '{entity.name}',"
             f" на {add_effect_schema.times} {form.get_genitive_turn_word(add_effect_schema.times)}\n")

    return text + "\n"



async def _add_stat_effect(
        entity: BaseCharacterModel,
        add_effect_schema: EffectSchema,
        effect: StatModifierEffect
) -> str:
    # Проверка, нет ли эффекта с такой же или большей продолжительностью на цели
    effects = await _get_effects(entity)
    if not await _check_add_possibility(effects, add_effect_schema, effect):
        return f"Эффект '{get_stat_modifier_effect_view(effect)}' большей или такой же продолжительности уже наложен на цель\n\n"

    await _add_effect_to_entity(
        entity=entity,
        effects=effects,
        effect_schema=add_effect_schema,
        effect=effect
    )

    return (f"Эффект модификации характеристики '{get_stat_modifier_effect_view(effect)}'"
            f" наложен на {entity.name},"
            f" на {add_effect_schema.times} {form.get_genitive_turn_word(add_effect_schema.times)}\n\n")




async def _apply_effects_on_entity(game_model: GameModel, entity: MobModel, event: str) -> str:
    effects = await _get_effects(entity)
    text = ""
    for effect_schema in effects[:]:
        # Проверяем event
        if effect_schema.event != event:
            continue

        # Определяем владельца и формируем Meta
        if effect_schema.caster_id is None:
            caster = game_model.character
        else:
            caster = entity

        effect_cls: type[BaseEffect] = effect_system.get_effect_by_url( effect_schema.effect_url )
        effect: BaseEffect = effect_cls()
        effect._form_effect_meta(
            game_model=game_model,
            room_model=game_model.room,
            player_char=game_model.character,
            caster=caster,
            target=entity,
        )

        # Применяем эффект
        if effect_schema.effect_type == BaseEffect.Type.TICK_EFFECT:
            effect: TickEffect
            text += effect.tick()

        # Обновляем таймер
        if effect_schema.times != -1:
            effect_schema.times -= 1
            if effect_schema.times <= 0:
                effects.remove( effect_schema )


    _update_entity_effects_field(entity, effects)


    return text + "\n"



def _update_entity_effects_field(entity: MobModel, effects: list[EffectSchema]):
    new_effects = []
    for schema in effects:
        effect_dict = schema.model_dump()
        new_effects.append( effect_dict )
    entity.effects = new_effects



async def _get_effects(entity: BaseCharacterModel) -> list[EffectSchema]:
    effects = []
    for effect_dict in entity.effects:
        schema = EffectSchema( **effect_dict )
        effects.append( schema )
    return effects


async def _check_add_possibility(
        effects: list[EffectSchema],
        new_effect_schema: EffectSchema,
        effect: BaseEffect
) -> bool:
    if not effect.updatable:
        return True
    for effect_schema in effects:
        if effect_schema.effect_url == new_effect_schema.effect_url:
            if effect_schema.times >= new_effect_schema.times:
                return False
    return True


async def _add_effect_to_entity(
        entity: BaseCharacterModel,
        effects: list[EffectSchema],
        effect_schema: EffectSchema,
        effect: BaseEffect,
):
    if effect.updatable:
        await _remove_effect_by_type(effects, effect_schema.effect_type, True)

    effects.append( effect_schema )

    new_effects = [ef_schema.model_dump() for ef_schema in effects]
    entity.effects = new_effects




async def _remove_effect_by_type(effects: list[EffectSchema], effect_type: str, all: bool = False):
    for effect in effects:
        if effect.effect_type == effect_type:
            effects.remove( effect )
            if not all:
                return