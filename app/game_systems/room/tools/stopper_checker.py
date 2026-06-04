from app.models.room import RoomModel
from game_data import const

def check_stopper(
        room_model: RoomModel,
        expect_stoppers: list[str | list] | str | None,
) -> bool:
    """
        Проверяет состояние room_model.stoppers на точное соответствие шаблону
         - stoppers = [], expect = None -> True
         - stoppers = ["s1"], expect = None -> False
         - stoppers = ["s1"], expect = "s1" -> True
         - stoppers = ["s1", "s2"], expect = "s1" -> False
         - stoppers = ["s1"], expect = ["s1", "s2"] -> False
         - stoppers = ["s1", "s2"], expect = ["s1", "s2"] -> True

         - stoppers = ["s1", "s2"], expect = ["s1", ["s2", "s3", "s4"]] -> True
    """

    stoppers = room_model.stoppers.copy()

    if expect_stoppers is None:
        return len(stoppers) == 0

    if isinstance(expect_stoppers, str):
        expect_stoppers = [ expect_stoppers ]
    else:
        expect_stoppers = list( expect_stoppers )

    if len(stoppers) != len(expect_stoppers):
        return False


    for expect_stopper in expect_stoppers:

        if isinstance(expect_stopper, list):
            stopper_element = None

            for available_stopper in expect_stopper:
                if available_stopper in stoppers:
                    stopper_element = available_stopper
                    break

            if stopper_element is None:
                return False

            index = stoppers.index(stopper_element)
            stoppers.pop( index )


        else:
            if expect_stopper not in stoppers:
                return False

            index = stoppers.index(expect_stopper)
            stoppers.pop( index )

    return True



def get_stopper_in_list(
        room_model: RoomModel,
        stopper_list: list[str] | str,
) -> str:
    """
        Возвращает стоппер из стопперов в комнате, который подходит под шаблон в списке

        Например, мы знаем что в стопперах в комнате есть указатель на цель, например ENEMY_POINTER_2.
        Мы хотим его получить, чтобы в будущем преобразовать в число, для этого мы передаем список со всеми указателями.
        И если в room.stoppers будет указатель подпадающий под шаблон в списке, он вернется. Иначе NONE_CONST
    """

    if isinstance(stopper_list, str):
        stopper_list = [stopper_list]

    stoppers = room_model.stoppers.copy()

    for stopper in stoppers:
        if stopper in stopper_list:
            return stopper

    return const.NONE_CONST