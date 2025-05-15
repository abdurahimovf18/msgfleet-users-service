from src.users_service.utils.dto import BaseDTO, s


class CreateUserDTO(BaseDTO):
    language: s.UserProfile.language
    