from app.models.general import ProfileModel

def get_sign_up_text(
    profile_model: ProfileModel,
) -> str:

    return f"""
        Профиль успешно создан
        
            id = {profile_model.id} 
            name = {profile_model.name}
            password = {profile_model.password}
            
            
    """


def get_sign_in_text(
        profile_model: ProfileModel,
) -> str:

    return f"""
        Вы успешно вошли в профиль
            
            id = {profile_model.id}
            name = {profile_model.name}
    """
