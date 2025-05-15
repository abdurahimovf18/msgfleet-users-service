from src.users_service.utils.dto import BaseDTO, s


class CreateDTO(BaseDTO):
    language: s.UserProfile.language
