from app.models.game import GameModel
from app.models.world import WorldModel

def get_world_text(
        base_url: str,
        world_model: WorldModel,
) -> str:
    return f"""
        Вы сейчас находитесь в мире
        
        
        Вы можете пойти в рейд, охотится на гоблинов
        Для этого пропишите 
        
        {base_url}world/start_raid/goblin_forest
    """