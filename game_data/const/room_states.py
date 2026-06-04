

class RoomStates:

    class General:
        INIT = "Init"
        TEXT = "Text"
        LEAVE = "Leave"


    class Battle:
        ENEMIES_BEFORE_PLAYER = "Enemies before player"
        PLAYER_TURN = "Player turn"
        ENEMIES_AFTER_PLAYER = "Enemies after player"

        END_OF_BATTLE = "End of battle"