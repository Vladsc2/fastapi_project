from game_data.items.items_system import _items
from game_data.templates.items import BaseItem

def main():
    saved_base_cls = None
    cls: BaseItem
    for url, cls in _items.items():
        base_cls = cls.__bases__[0].__name__
        if base_cls != saved_base_cls:
            saved_base_cls = base_cls
            print(f"Тип предметов {saved_base_cls}")

        print( f"  {url}" )


if __name__ == '__main__':
    main()