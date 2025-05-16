from src.users_service.utils.dto import BaseDTO, s


class CreateUserDTO(BaseDTO):
    id: s.User.id
    created_at: s.User.created_at
    updated_at: s.User.updated_at
    language: s.UserProfile.language
