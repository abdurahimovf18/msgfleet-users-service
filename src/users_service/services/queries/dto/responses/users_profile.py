from src.users_service.utils.dto import BaseDTO, s


class CreateDTO(BaseDTO):
    user_id: s.UserProfile.user_id
    language: s.UserProfile.language
    is_active: s.UserProfile.is_active
    is_deleted: s.UserProfile.is_deleted
    