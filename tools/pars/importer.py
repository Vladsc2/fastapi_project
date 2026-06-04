import importlib
import os


async def get_first_cls_name(
        file_path: str,
        parent_cls: str | None = None,
) -> str | None:

    if not os.path.isfile( file_path ):
        return None

    lines: list[str]
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()

        if not line.startswith("class"):
            continue

        if not ("(" in line and ")" in line):
            continue


        left_parenthesis = line.find("(")
        right_parenthesis = line.find(")")

        class_name = line[:left_parenthesis]
        class_name = class_name[len("class"):]
        class_name = class_name.strip()

        if parent_cls is not None:
            parent_cls_line = line[left_parenthesis+1:right_parenthesis]
            parent_cls_line = parent_cls_line.strip()
            if parent_cls_line != parent_cls:
                continue

        return class_name



async def import_class(
        abs_path: str,
        class_name: str,
):
    dotted_path: str = await _abs_path_to_dotted( abs_path )
    module = importlib.import_module(dotted_path)

    cls = getattr(module, class_name)

    return cls



async def _abs_path_to_dotted(abs_path: str) -> str:
    """
    Преобразует абсолютный путь к .py-файлу в dotted-путь Python.
    Пример:
        D:\\...\\game_data\\raids_data\\goblin_forest\\rooms\\battle\\one_base_goblin.py
        -> game_data.raids_data.goblin_forest.rooms.battle.one_base_goblin
    """
    # Нормализуем слеши под текущую ОС
    abs_path = os.path.normpath(abs_path)

    # Находим часть пути, начиная с 'game_data'
    parts = abs_path.split(os.sep)
    try:
        idx = parts.index("game_data")
    except ValueError:
        raise ValueError(
            f"Путь не содержит 'game_data': {abs_path}\n"
            "Убедитесь, что файл находится внутри пакета game_data."
        )

    # Берём всё, начиная с game_data, и отрезаем расширение .py
    relevant = parts[idx:]                     # ['game_data', 'raids_data', ..., 'one_base_goblin.py']
    relevant[-1] = os.path.splitext(relevant[-1])[0]  # убираем .py у последнего элемента
    dotted = ".".join(relevant)
    return dotted