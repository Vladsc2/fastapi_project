from game_data.templates.items import JunkItem

class Board( JunkItem ):
    id = "board"

    name = "Доска"
    desc = "Деревянная доска, можно продать в городе"

    sell_price = 2
    buy_price = 5

    stack_limit = 10