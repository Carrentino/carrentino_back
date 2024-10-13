from core.types import Choices


class USER_ROLES(Choices):
    """Choices of user roles"""
    PERSON = "PS"
    COMPANY = "CM"
    ADMIN = "AD"

    CHOICES = (
        (PERSON, "Физ. Лицо"),
        (COMPANY, "Компания"),
        (ADMIN, "Админ")
    )