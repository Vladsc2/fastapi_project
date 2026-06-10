from game_data.templates.items import JunkItem

class BrokenArrow( JunkItem ):
    id = "broken_arrow"

    name = "Сломанная стрела"
    desc = "Сломанная стрела. Её уже не восстановить, но можно продать за небольшие деньги"

    sell_price = 1
    buy_price = 5

    stack_limit = 20