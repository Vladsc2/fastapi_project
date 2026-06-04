from app.models.general import IpAssociationsModel
from app.core.config import config

def get_home_text(
        base_url: str,
        ip_association: IpAssociationsModel | None,
) -> str:

    if ip_association is None:
        text = _get_pure_home_text(base_url)

    else:
        text = _get_have_ip_association_home_text(base_url, ip_association)


    return text



def _get_pure_home_text(base_url: str) -> str:
    return f"""
        Добро пожаловать в {config.game_name}!
        
        Это небольшая текстовая браузерная игра,
         с пошаговыми действиями, и системой коллекционирования и прокачки
        
        {_get_create_profile_string(base_url)}
    """



def _get_have_ip_association_home_text(base_url: str, ip_association: IpAssociationsModel) -> str:
    string = f"""
        С возвращением в мир {config.game_name}!
        
        Ваш ip_address: {ip_association.ip_address}
        """

    if ip_association.profile is None:
        string += f"""
        С данным ip адресом не ассоциирован не один профиль
            
        {_get_create_profile_string(base_url)}
        """.strip()
    else:
        string += f"""
        Ваш ассоциированный профиль: {ip_association.profile.name}
        
        Игры:
            Слот 1: {ip_association.profile.first_game_id}
            Слот 2: {ip_association.profile.second_game_id}
            Слот 3: {ip_association.profile.third_game_id}
            
            Активная игра: {ip_association.profile.active_game_id}
        """.strip()

        string += f"""
        
            Создать новую игру:
            
            {base_url}game/create?game_slot=SLOT&character_name=CHAR_NAME
            
            Установить существующую игру как активную:
            
            {base_url}game/set_active?game_slot=SLOT
            
            Удалить существующую игру:
            
            {base_url}game/delete?game_slot=SLOT
        """.rstrip()


    return string



def _get_create_profile_string(base_url: str) -> str:
    return f"""
        Для создания нового профиля введите:
        {base_url}profile/sign_up?name=USERNAME&password=PASSWORD
         Замени USERNAME и PASSWORD на твои имя пользователя и пароль
         
        Для входа в существующий профиль введите:
        {base_url}profile/sign_in?name=USERNAME&password=PASSWORD
         Замени USERNAME и PASSWORD на твои имя пользователя и пароль
    """.strip()