from game_data.items import items_system    # Прогружаем предметы
from game_data.scripts import scripts_system
from game_data.effects import effect_system

from fastapi import FastAPI
import uvicorn

from app.routers.general import home_router, profile_auth_router, profile_router
from app.routers.game import init_game_router
from app.routers.world import world_router, create_raid_router
from app.routers.raid import raid_router
from app.routers.raid import raid_select_room_router
from app.routers.room import room_router
from app.routers.room import room_exit_router
from app.routers.roll import roll_router
from app.routers.room import room_battle_router

app = FastAPI()
app.include_router( home_router )
app.include_router( profile_auth_router )
app.include_router( profile_router )
app.include_router( init_game_router )
app.include_router( world_router )
app.include_router( create_raid_router )
app.include_router( raid_router )
app.include_router( raid_select_room_router )
app.include_router( room_router )
app.include_router(room_exit_router)
app.include_router( roll_router )
app.include_router( room_battle_router )


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)

