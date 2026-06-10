from app.models.game import GameModel, BaseCharacterModel, MobModel
from app.schemas.script import ScriptSchema
from game_data.scripts import scripts_system
from game_data.templates.script import BaseScript


async def add_script_to_entity(entity: BaseCharacterModel, url: str):
    script_cls: type[BaseScript] = scripts_system.get_script_by_url(url)

    if script_cls is None:
        print(f"Error: Не удалось получить скрипт по url '{url}'\n"
              f" - {__file__}")
        return
    if not hasattr(script_cls, "trigger"):
        print( f"Error: У скрипта '{script_cls.__name__}' не создано поле trigger\n"
               f" - {__file__}" )
        return

    script_schema = ScriptSchema(trigger=script_cls.trigger, url=url, only_one=script_cls.only_one)

    entity.scripts.append( script_schema.model_dump() )




async def execute_script_by_trigger(
        game_model: GameModel,
        owner: BaseCharacterModel,
        enemies: list[MobModel],
        trigger: str,
):
    for script_dict in owner.scripts[:]:
        script_schema = ScriptSchema.model_validate( script_dict )

        if script_schema.trigger != trigger:
            continue

        script_cls: type[BaseScript] = scripts_system.get_script_by_url( script_schema.url )
        script = script_cls()
        script._form_script_meta(
            game_model=game_model,
            owner=owner,
            enemies=enemies,
        )
        await script.run()

        if script_cls.only_one:
            owner.scripts.remove( script_dict )