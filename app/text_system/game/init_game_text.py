from app.models.game import GameModel

def get_create_game_text(
        game_slot: int,
        game_model: GameModel,
) -> str:
    return f"""
        Создана игра в слоте {game_slot}
            - game_id = {game_model.id}
    """


def get_set_active_game_text(
        game_slot: int,
        game_id: int,
) -> str:
    return f"""
        Активная игра установлена
            - Слот игры {game_slot}
            - id игры {game_id}
    """


def get_delete_game_text(
        game_slot: int,
        game_id: int,
) -> str:
    return f"""
        Игра в слоте '{game_slot}' была удалена
    """